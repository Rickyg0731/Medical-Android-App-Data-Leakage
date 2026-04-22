# ─────────────────────────────────────────────────────────────────────────────
# config.py — Detection dictionary for the Android Privacy Leak Analyzer
# Add or remove entries here to tune what the scanner looks for.
# ─────────────────────────────────────────────────────────────────────────────

# Sensitive data SOURCES — Android APIs that access private user data.
# Organized by category for readability.
SENSITIVE_SOURCES = [
    # Device identity
    "getDeviceId",
    "getImei",
    "getAndroidId",
    "getSubscriberId",       # IMSI / carrier ID
    "getLine1Number",        # phone number
    "getSimSerialNumber",
    "getInstalledPackages",
    "getInstalledApplications",

    # Location
    "getLastKnownLocation",
    "getLatitude",
    "getLongitude",
    "requestLocationUpdates",
    "getCurrentLocation",

    # Health & fitness (expanded for this project)
    "getHeartRate",
    "getStepCount",
    "getStepCounterSensor",  # step counter sensor registration
    "getCaloriesBurned",
    "getSleepData",
    "getWeight",
    "getBodyFat",
    "getBloodPressure",
    "getBloodOxygen",
    "getDistance",
    "getActiveMinutes",

    # Biometrics / camera
    "getFaceData",
    "getBiometricData",
    "takePicture",

    # Accounts / contacts
    "getAccounts",
    "getContactsProvider",

    # Bluetooth (wearables like fitness bands, heart rate monitors)
    "BluetoothGatt",
    "connectGatt",
    "discoverServices",
    "readCharacteristic",
]

# Data SINKS — APIs that transmit, log, or persist data externally.
SINKS = [
    # Network transmission
    "HttpURLConnection",
    "OkHttpClient",
    "Retrofit",
    "Socket",
    "URLConnection",
    "HttpsURLConnection",
    "AsyncHttpClient",
    "Volley",

    # Logging (can expose data in logcat)
    "Log.d",
    "Log.e",
    "Log.i",
    "Log.v",
    "Log.w",

    # Local storage / file output
    "FileOutputStream",
    "SharedPreferences",
    "SQLiteDatabase",
    "ContentResolver",

    # Clipboard / intent
    "ClipboardManager",
    "sendBroadcast",
    "startActivity",
]

# Known third-party analytics, advertising, and tracking libraries.
# Key = display name, Value = package prefix found in source code.
THIRD_PARTY_LIBS = {
    "Firebase Analytics":   "com.google.firebase",
    "Firebase Crashlytics": "com.google.firebase.crashlytics",
    "Google AdMob":         "com.google.android.gms.ads",
    "Google Play Services": "com.google.android.gms",
    "Facebook SDK":         "com.facebook",
    "Mixpanel":             "com.mixpanel",
    "Amplitude":            "com.amplitude",
    "Segment":              "com.segment.analytics",
    "AppsFlyer":            "com.appsflyer",
    "Adjust":               "com.adjust.sdk",
    "Branch":               "io.branch",
    "OneSignal":            "com.onesignal",
    "Sentry":               "io.sentry",
    "Intercom":             "io.intercom",
    "Braze (Appboy)":       "com.appboy",
    "Leanplum":             "com.leanplum",
}

# Regex to find URLs in source code (http and https)
URL_REGEX = r'https?://[^\s"\'<>]+'
