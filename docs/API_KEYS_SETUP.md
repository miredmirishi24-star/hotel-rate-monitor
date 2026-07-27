# 🔑 API KEYS SETUP GUIDE

This guide will help you get all the necessary API keys to run the hotel rate monitor.

## 1. EXPEDIA API (via RapidAPI)

### Step 1: Sign up on RapidAPI
1. Go to https://rapidapi.com/
2. Click "Sign Up" and create an account
3. Verify your email

### Step 2: Find Expedia/Booking API
1. Search for "Booking.com" in the RapidAPI marketplace
2. Look for the API by `apidojo` (most popular)
3. Click "Subscribe"

### Step 3: Get Your API Key
1. After subscribing, go to your API's dashboard
2. Look for "API Key" or "X-RapidAPI-Key"
3. Copy this key

### Step 4: Update .env
```bash
EXPEDIA_API_KEY=your_copied_key_here
```

**API Endpoint** (if needed):
```
https://booking-com.p.rapidapi.com/v1/hotels/search
```

---

## 2. BOOKING.COM API

### Step 1: Register for Developer Access
1. Go to https://developer.booking.com/
2. Click "Get Started" or "Apply"
3. Fill out the application form
4. Agree to terms

### Step 2: Create an Application
1. Log in to your Booking.com partner account
2. Go to Settings → API
3. Click "Create New Application"
4. Fill in:
   - Application Name: "Hotel Rate Monitor"
   - Website: Your website or GitHub repo URL
   - Support Email: Your email

### Step 3: Get API Credentials
1. Your application shows:
   - **API Key**: Copy this
   - **Secret**: Copy this
2. Save both securely

### Step 4: Update .env
```bash
BOOKING_API_KEY=your_api_key_here
```

**API Documentation**: https://developer.booking.com/documentation

---

## 3. TRIP.COM API

### Step 1: Register on Trip.com OpenAPI
1. Go to https://www.trip.com/openapi/
2. Click "Free Trial" or "Apply"
3. Create account with email

### Step 2: Get API Credentials
1. Log in to Trip.com partner portal
2. Go to My Applications
3. Click "Create Application"
4. Select "Hotel Search API"
5. Accept terms

### Step 3: Retrieve API Key
1. Find your app in "My Applications"
2. Click it to view details
3. Copy the **API Key** and **Secret**

### Step 4: Update .env
```bash
TRIP_API_KEY=your_trip_api_key_here
```

**Note**: Trip.com may require additional documentation. Response time is 2-5 business days.

---

## 4. GDS (GLOBAL DISTRIBUTION SYSTEM) API

### Option A: Amadeus GDS

1. Go to https://developers.amadeus.com/
2. Sign up for free account
3. Create an application
4. Get your **Client ID** and **Client Secret**
5. Update .env:
```bash
GDS_API_KEY=your_amadeus_client_id:your_amadeus_client_secret
```

### Option B: SABRE GDS

1. Visit https://developer.sabre.com/
2. Register for developer program
3. Create an app in dashboard
4. Get API credentials
5. Update .env:
```bash
GDS_API_KEY=your_sabre_api_key_here
```

---

## 📋 Complete .env Template

Create a `.env` file in your project root with all keys:

```bash
# API Keys
EXPEDIA_API_KEY=your_expedia_key_from_rapidapi
BOOKING_API_KEY=your_booking_com_api_key
TRIP_API_KEY=your_trip_com_api_key
GDS_API_KEY=your_gds_key_here

# Google Sheets (we'll set this up next)
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_FILE=./credentials.json
```

---

## ✅ Verify Your Keys

Run this to test:

```bash
python -c "from config import EXPEDIA_API_KEY, BOOKING_API_KEY, TRIP_API_KEY, GDS_API_KEY; print('✓ All keys loaded')"
```

---

## 🚨 IMPORTANT: Keep Keys Secure

⚠️ **NEVER commit .env to Git!**

The `.gitignore` file already excludes it. Verify:

```bash
cat .gitignore | grep .env
```

---

## 💡 Free Tier Limits

| API | Free Requests/Month | Cost After |
|-----|-------------------|------------|
| Expedia (RapidAPI) | Varies | $0.01-0.05/req |
| Booking.com | 1,000 | Contact sales |
| Trip.com | 100 | Contact sales |
| Amadeus GDS | 10,000/year | Paid tiers |

---

## ❓ Troubleshooting

### "Invalid API Key" Error
- Verify key is copied correctly (no extra spaces)
- Check key hasn't expired
- Ensure you're using the right environment (sandbox vs production)

### "Rate limit exceeded"
- Wait before next request
- Upgrade to paid tier
- Reduce CHECK_INTERVAL in config.py

### "401 Unauthorized"
- API key may be invalid
- Check if subscription is active
- Some APIs require additional headers (verify docs)

---

## 📚 Reference Links

- RapidAPI: https://rapidapi.com/
- Booking.com Dev: https://developer.booking.com/
- Trip.com OpenAPI: https://www.trip.com/openapi/
- Amadeus Dev: https://developers.amadeus.com/
- SABRE Dev: https://developer.sabre.com/
