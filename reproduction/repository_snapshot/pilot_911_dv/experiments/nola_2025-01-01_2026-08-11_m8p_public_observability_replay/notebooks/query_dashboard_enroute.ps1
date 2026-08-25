param(
    [string]$Entity = "FACT Call for Service",
    [string]$Property = "Incident_To_EnRoute_Seconds",
    [string]$OutputPath = "C:\AI Project\RA_Topic\pilot_911_dv\source_data\official_event_context\nopd_current_public_architecture\2026-08-11\nopd_response_times_powerbi_enroute_aggregate.json"
)

$ErrorActionPreference = "Stop"

$endpoint = "https://wabi-us-gov-virginia-api.analysis.usgovcloudapi.net/public/reports/querydata?synchronous=true"
$resourceKey = "b5330cbb-48ab-42fe-8228-01e3d60735ec"
$body = @{
    version = "1.0.0"
    queries = @(
        @{
            Query = @{
                Commands = @(
                    @{
                        SemanticQueryDataShapeCommand = @{
                            Query = @{
                                Version = 2
                                From = @(
                                    @{ Name = "x"; Entity = $Entity; Type = 0 }
                                    @{ Name = "m"; Entity = "Facts"; Type = 0 }
                                )
                                Select = @(
                                    @{
                                        Column = @{
                                            Expression = @{ SourceRef = @{ Source = "x" } }
                                            Property = $Property
                                        }
                                        Name = "$Entity.$Property"
                                    }
                                    @{
                                        Measure = @{
                                            Expression = @{ SourceRef = @{ Source = "m" } }
                                            Property = "Count of Dispatch Incidents"
                                        }
                                        Name = "Facts.Count of Dispatch Incidents"
                                    }
                                )
                                OrderBy = @(
                                    @{
                                        Direction = 2
                                        Expression = @{
                                            Measure = @{
                                                Expression = @{ SourceRef = @{ Source = "m" } }
                                                Property = "Count of Dispatch Incidents"
                                            }
                                        }
                                    }
                                )
                            }
                            Binding = @{
                                DataReduction = @{
                                    DataVolume = 3
                                    Primary = @{ Window = @{ Count = 20 } }
                                }
                                Primary = @{ Groupings = @(@{ Projections = @(0, 1) }) }
                                Version = 1
                            }
                            ExecutionMetricsKind = 1
                        }
                    }
                )
            }
            CacheKey = ""
            ApplicationContext = @{ DatasetId = "1300399" }
        }
    )
    cancelQueries = @()
    modelId = 1300399
} | ConvertTo-Json -Depth 30 -Compress

$headers = @{
    "X-PowerBI-ResourceKey" = $resourceKey
    "Origin" = "https://app.powerbigov.us"
    "Referer" = "https://app.powerbigov.us/"
    "ActivityId" = [guid]::NewGuid().ToString()
    "RequestId" = [guid]::NewGuid().ToString()
}

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
try {
    foreach ($entry in $headers.GetEnumerator()) {
        [void]$client.DefaultRequestHeaders.TryAddWithoutValidation($entry.Key, [string]$entry.Value)
    }
    $content = [System.Net.Http.StringContent]::new($body, [System.Text.Encoding]::UTF8, "application/json")
    $response = $client.PostAsync($endpoint, $content).GetAwaiter().GetResult()
    $responseBody = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    if (-not $response.IsSuccessStatusCode) {
        throw "Power BI aggregate query failed with HTTP $([int]$response.StatusCode): $responseBody"
    }
    [System.IO.File]::WriteAllText($OutputPath, $responseBody, [System.Text.UTF8Encoding]::new($false))
}
finally {
    $client.Dispose()
}
Get-Item -LiteralPath $OutputPath | Select-Object FullName, Length, LastWriteTime
