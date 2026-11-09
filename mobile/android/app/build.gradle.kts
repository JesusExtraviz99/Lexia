plugins { id("com.android.application") }
android {
    namespace = "es.lexia.piloto"
    compileSdk = 36
    buildToolsVersion = "35.0.0"
    defaultConfig {
        applicationId = "es.lexia.piloto"
        minSdk = 26
        targetSdk = 35
        versionCode = 5
        versionName = "0.5-piloto"
        ndk { abiFilters += "arm64-v8a" }
    }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_11; targetCompatibility = JavaVersion.VERSION_11 }
    buildTypes { getByName("release") { isMinifyEnabled = false } }
}
dependencies { implementation("ai.moonshine:moonshine-voice:0.1.5") }
dependencyLocking { lockAllConfigurations() }
