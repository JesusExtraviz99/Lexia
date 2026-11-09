param(
    [string]$SdkPath = "$env:LOCALAPPDATA/Android/Sdk",
    [string]$JdkPath = "$env:ProgramFiles/Android/Android Studio/jbr",
    [string]$GradlePath = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$androidProject = Join-Path $projectRoot 'mobile/android'
if (-not $GradlePath) {
    $candidate = Get-ChildItem -LiteralPath (Join-Path $env:USERPROFILE '.gradle/wrapper/dists/gradle-8.13-bin') -Filter gradle.bat -Recurse | Select-Object -First 1
    if (-not $candidate) { throw 'No se encuentra Gradle 8.13; indica -GradlePath con la ruta a gradle.bat.' }
    $GradlePath = $candidate.FullName
}
if (-not (Test-Path -LiteralPath (Join-Path $JdkPath 'bin/java.exe'))) { throw 'No se encuentra el JDK indicado.' }
if (-not (Test-Path -LiteralPath (Join-Path $SdkPath 'platforms/android-36/android.jar'))) { throw 'Falta Android SDK platform 36.' }
$sdkNormalized = $SdkPath.Replace('\','/').Replace(':','\:')
[IO.File]::WriteAllText((Join-Path $androidProject 'local.properties'),"sdk.dir=$sdkNormalized`n",[Text.UTF8Encoding]::new($false))
$previousJavaHome = $env:JAVA_HOME
try {
    $env:JAVA_HOME = $JdkPath
    & $GradlePath -p $androidProject --no-daemon --console plain assembleDebug lintDebug --write-locks
    if ($LASTEXITCODE -ne 0) { throw "Compilación/verificación fallida: $LASTEXITCODE" }
    Write-Output (Join-Path $androidProject 'app/build/outputs/apk/debug/app-debug.apk')
} finally { $env:JAVA_HOME = $previousJavaHome }
