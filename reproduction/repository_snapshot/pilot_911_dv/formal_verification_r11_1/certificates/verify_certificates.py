"""Verify exact-rational primal/dual certificates without an LP solver.

The committed certificate is deliberately a checker fixture. The frozen M6C
artifact located during this pass states NOT_CERTIFIED_RESOURCE_BLOCKED and
contains no admissible primal/dual vectors, so this package does not promote a
paper-level computational claim.
"""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "lp_inputs" / "checker_fixture_input.json"
DEFAULT_CERTIFICATE = ROOT / "lp_certificates" / "checker_fixture_certificate.json"


class CertificateError(ValueError):
    pass


def fraction(value: Any) -> Fraction:
    if not isinstance(value, (str, int)):
        raise CertificateError(f"not an exact rational literal: {value!r}")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise CertificateError(f"invalid exact rational literal: {value!r}") from exc


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    if len(left) != len(right):
        raise CertificateError("dot-product dimension mismatch")
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def verify(model: dict[str, Any], certificate: dict[str, Any]) -> dict[str, str]:
    if model.get("sense") != "min":
        raise CertificateError("only minimization certificates are supported")
    if model.get("constraint_form") != "A x >= b; x >= 0":
        raise CertificateError("unexpected primal constraint form")
    if model.get("dual_form") != "A^T y <= c; y >= 0":
        raise CertificateError("unexpected dual constraint form")

    matrix = [[fraction(v) for v in row] for row in model["A"]]
    b = [fraction(v) for v in model["b"]]
    c = [fraction(v) for v in model["c"]]
    if not matrix or not c or len(matrix) != len(b):
        raise CertificateError("empty or inconsistent LP dimensions")
    if any(len(row) != len(c) for row in matrix):
        raise CertificateError("matrix row width does not match objective")

    x = [fraction(v) for v in certificate["primal"]["x"]]
    y = [fraction(v) for v in certificate["dual"]["y"]]
    if len(x) != len(c) or len(y) != len(b):
        raise CertificateError("certificate vector dimension mismatch")
    if any(v < 0 for v in x):
        raise CertificateError("primal nonnegativity violated")
    if any(v < 0 for v in y):
        raise CertificateError("dual nonnegativity violated")

    primal_lhs = [dot(row, x) for row in matrix]
    if any(lhs < rhs for lhs, rhs in zip(primal_lhs, b, strict=True)):
        raise CertificateError("primal feasibility violated")

    dual_lhs = [
        dot([matrix[row][column] for row in range(len(matrix))], y)
        for column in range(len(c))
    ]
    if any(lhs > rhs for lhs, rhs in zip(dual_lhs, c, strict=True)):
        raise CertificateError("dual feasibility violated")

    primal_objective = dot(c, x)
    dual_objective = dot(b, y)
    claimed_primal = fraction(certificate["primal"]["claimed_objective"])
    claimed_dual = fraction(certificate["dual"]["claimed_objective"])
    if primal_objective != claimed_primal:
        raise CertificateError("claimed primal objective does not match c*x")
    if dual_objective != claimed_dual:
        raise CertificateError("claimed dual objective does not match b*y")
    if primal_objective != dual_objective:
        raise CertificateError("primal and dual objectives do not match")

    return {
        "status": "CERTIFICATE_VERIFIED",
        "scope": certificate.get("scope", "unspecified"),
        "primal_objective": str(primal_objective),
        "dual_objective": str(dual_objective),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--skip-negative-check", action="store_true")
    args = parser.parse_args()

    model = json.loads(args.input.read_text(encoding="utf-8"))
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    result = verify(model, certificate)

    if not args.skip_negative_check:
        forged = copy.deepcopy(certificate)
        forged["primal"]["x"][0] = "1"
        try:
            verify(model, forged)
        except CertificateError:
            result["forgery_negative_check"] = "REJECTED_AS_REQUIRED"
        else:
            raise CertificateError("forged certificate was accepted")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
