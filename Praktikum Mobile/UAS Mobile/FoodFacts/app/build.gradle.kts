plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    id("org.jetbrains.kotlin.plugin.serialization") version "1.9.10" // Untuk kotlinx.serialization
    id("kotlin-kapt") // ✅ Wajib untuk Room
}

android {
    namespace = "com.presca.foodfacts"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.presca.foodfacts"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = "11"
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    // Jetpack Compose & Material 3
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation("androidx.compose.material:material-icons-extended") // Sudah ada
    implementation("androidx.security:security-crypto:1.1.0-alpha06")

    // Navigation Compose
    implementation("androidx.navigation:navigation-compose:2.7.7") // <--- DISARANKAN UPDATE KE VERSI TERBARU (sebelumnya 2.7.4)

    // ViewModel
    implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.7.0") // <--- DISARANKAN UPDATE KE VERSI TERBARU (sebelumnya 2.6.2)
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0") // <--- TAMBAHKAN INI UNTUK OBSERVASI FLOW DARI LIFECYCLE (jika belum ada)

    // Retrofit + KotlinX Serialization
    implementation("com.squareup.retrofit2:retrofit:2.9.0") // Sudah ada
    implementation("com.jakewharton.retrofit:retrofit2-kotlinx-serialization-converter:0.8.0") // Sudah ada
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0") // Sudah ada

    // OkHttp
    implementation("com.squareup.okhttp3:okhttp:4.10.0") // Sudah ada
    implementation("com.squareup.okhttp3:logging-interceptor:4.10.0") // Sudah ada

    // Coroutines
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3") // Sudah ada

    // Glide (Jetpack Compose)
    // Versi yang Anda gunakan (1.0.0-alpha.5) sudah agak lama.
    // Disarankan menggunakan versi beta atau rilis stabil jika ada.
    // Untuk saat ini, kita bisa pertahankan atau update ke 1.0.0-beta01 seperti yang kita diskusikan.
    implementation("com.github.bumptech.glide:compose:1.0.0-beta01") // <--- UPDATE INI (Opsional tapi direkomendasikan)
    // Anda membutuhkan annotation processor untuk Glide di tingkat aplikasi.
    // Tambahkan juga dependensi core Glide jika belum di-resolve secara transitif.
    implementation("com.github.bumptech.glide:glide:4.16.0") // <--- TAMBAHKAN INI (Versi terbaru)
    kapt("com.github.bumptech.glide:compiler:4.16.0") // <--- UPDATE VERSI INI AGAR SAMA DENGAN GLIDE CORE

    // Room Database
    implementation("androidx.room:room-runtime:2.6.1") // Sudah ada
    kapt("androidx.room:room-compiler:2.6.1") // Sudah ada
    implementation("androidx.room:room-ktx:2.6.1") // Sudah ada
    implementation("androidx.datastore:datastore-preferences:1.0.0") // Sudah ada, tidak terkait langsung tapi ok.

    // Unit testing & UI testing
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)
}