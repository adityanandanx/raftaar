# Product Requirements Document: Rapido Clone - Bike Sharing MVP

## Problem Statement

Users in urban areas need an affordable, convenient way to travel short distances without owning a bike. Currently, they rely on cars (expensive, congested), taxis (unsafe, unreliable), or public transport (limited routes). There is no easy-to-use, trusted bike-sharing platform in the market that offers:
- Transparent pricing
- Quick booking and trip completion
- Reliable bike availability and maintenance
- Trustworthy payment and refund policies

## Solution

Build a bike-sharing platform (Rapido clone) that allows users to:
1. **Find bikes** near their location via a map interface
2. **Reserve a bike** for 5 minutes
3. **Unlock and ride** by scanning a QR code
4. **Return the bike** to any station
5. **Get charged** automatically based on trip duration
6. **Request refunds** for issues without friction

Admins can:
- Manage bikes and stations
- View trip history, revenue, and utilization metrics
- Update pricing rules
- Handle support issues

The MVP covers **one city only** with station-based bikes (pick up and drop off at designated stations).

## User Stories

### **Customer: Finding & Booking**
1. As a customer, I want to see all nearby bike stations on a map, so that I can find the closest bike to me
2. As a customer, I want to filter stations by available bikes count, so that I don't waste time going to empty stations
3. As a customer, I want to reserve a bike for 5 minutes, so that I have time to walk to the station
4. As a customer, I want to cancel a reservation before I reach the station, so that I can book a different bike if needed
5. As a customer, I want to see the bike model and condition in the app, so that I can choose bikes I'm comfortable with
6. As a customer, I want real-time updates on bike availability (refreshed on-demand), so that I don't travel to a station with no bikes

### **Customer: Trip Execution**
7. As a customer, I want to unlock a bike by scanning a QR code or entering a code, so that I don't need a physical key
8. As a customer, I want the trip timer to start automatically when I unlock the bike, so that I know how much the trip will cost
9. As a customer, I want to pause/resume a trip, so that I can take a break without ending the trip
10. As a customer, I want to return a bike to any station (not just the origin), so that I have flexibility in my route
11. As a customer, I want the trip to end automatically when I lock the bike at a station, so that I don't have to manually end it

### **Customer: Payment & Billing**
12. As a customer, I want to save my card during signup, so that I don't have to enter it for every trip
13. As a customer, I want to see the estimated cost before booking, so that I can budget my trip
14. As a customer, I want to be charged based on actual trip duration with a hybrid model (base fee + per-minute), so that short trips are affordable
15. As a customer, I want to receive an itemized receipt after each trip, so that I can verify the charges
16. As a customer, I want to see my trip history with costs, so that I can track my spending
17. As a customer, I want to apply discount codes or promotional codes, so that I can get discounts on trips

### **Customer: Issues & Refunds**
18. As a customer, I want to report a damaged bike or issue during a trip, so that the platform knows about it
19. As a customer, I want an easy refund process if the trip was problematic (bike issues, accident), so that I don't get overcharged
20. As a customer, I want automatic refund eligibility based on a policy (e.g., refund if reported within 24 hours), so that I don't have to wait for support
21. As a customer, I want to contact support through the app, so that I don't have to make a phone call
22. As a customer, I want to view my support tickets and their status, so that I know when issues will be resolved

### **Customer: Account & Preferences**
23. As a customer, I want to update my profile (name, phone, email), so that my account information is current
24. As a customer, I want to receive SMS/email notifications for trip confirmations and receipts, so that I have proof of transactions
25. As a customer, I want to view my overall statistics (total trips, total distance, total spent), so that I can gamify or track my usage
26. As a customer, I want to set up emergency contacts, so that the platform can notify them if needed

### **Admin: Bike & Station Management**
27. As an admin, I want to create new stations with locations and bike capacity, so that I can expand the service to new areas
28. As an admin, I want to add bikes to stations, so that I can stock them with inventory
29. As an admin, I want to mark bikes as under maintenance, so that customers don't book broken bikes
30. As an admin, I want to retire bikes from the system, so that I can manage aging inventory
31. As an admin, I want to view the status of all bikes (available, in-use, maintenance, retired), so that I can plan operations
32. As an admin, I want to see which station has the lowest bike availability, so that I can prioritize restocking

### **Admin: Trip Monitoring**
33. As an admin, I want to view all trips in real-time, so that I can monitor platform activity
34. As an admin, I want to filter trips by date, user, station, or status, so that I can analyze specific patterns
35. As an admin, I want to see abandoned trips or trips with issues flagged, so that I can investigate problematic users or bikes
36. As an admin, I want to view the average trip duration by station, so that I can understand usage patterns

### **Admin: Financial & Reporting**
37. As an admin, I want to view total revenue for a given period, so that I can track business performance
38. As an admin, I want to see revenue by station, so that I can identify high-performing and underperforming locations
39. As an admin, I want to see the utilization rate of each bike (trips per bike per month), so that I can measure ROI
40. As an admin, I want to export trip data and financials as CSV/PDF, so that I can share reports with stakeholders
41. As an admin, I want to see refunds issued and reasons, so that I can identify systemic issues

### **Admin: Pricing & Promotions**
42. As an admin, I want to update the base fare, per-minute rate, and threshold minutes, so that I can adjust pricing dynamically
43. As an admin, I want to create and manage discount codes, so that I can run promotions
44. As an admin, I want to see which discount codes are most used, so that I can plan future promotions
45. As an admin, I want to set surge pricing rules (optional for MVP), so that I can optimize pricing during peak hours

### **Admin: Support & Disputes**
46. As an admin, I want to view all support tickets, so that I can respond to customer issues
47. As an admin, I want to approve or reject refund requests with notes, so that I can manage disputes fairly
48. As an admin, I want to escalate tickets to higher priority, so that urgent issues get addressed faster
49. As an admin, I want to see customer complaint trends, so that I can identify and fix recurring issues

### **Admin: User Management**
50. As an admin, I want to view all registered users and their activity, so that I can identify power users or problematic accounts
51. As an admin, I want to suspend or block users for violations, so that I can maintain platform safety
52. As an admin, I want to view user payment history and failed transactions, so that I can follow up on billing issues

## Implementation Decisions

### **Architecture & Tech Stack**
- **Backend:** Python + FastAPI with async/await support for scalability
- **Database:** PostgreSQL with PostGIS extension for geospatial queries
- **Frontend:** React web app (mobile can be added in v2)
- **Payment:** Razorpay integrated for payment processing and refunds
- **Deployment:** Docker containerized, deployed on Fly.io or Railway
- **Real-time Updates:** REST API + client-side polling (30-second refresh) for MVP

### **Core Modules**
The backend is organized into 9 core modules, each with a clean, testable interface:

1. **Authentication & User Management:** User registration, login, profile management, card tokenization
2. **Bike & Station Management:** CRUD operations for bikes and stations, availability tracking
3. **Booking & Reservation:** 5-minute bike reservation, trip start/end logic
4. **Pricing & Billing:** Trip cost calculation using hybrid model (base fee + per-minute)
5. **Payment Processing:** Razorpay integration, card authorization, charging, refunds
6. **Trip History & Analytics:** Trip logging, utilization metrics, revenue reports
7. **Admin & Operations:** Dashboard access, bike/station/pricing management, support ticket handling
8. **Geolocation & Map:** PostGIS-based spatial queries (find nearby bikes, closest stations)
9. **Notification & Support:** Email/SMS notifications, support ticket creation and management

### **Database Schema**
Key tables:
- `users` (id, email, phone, hashed_password, created_at)
- `payment_methods` (id, user_id, razorpay_token, is_default)
- `stations` (id, name, latitude, longitude, capacity, created_at)
- `bikes` (id, station_id, qr_code_hash, status, model, created_at, last_maintenance)
- `reservations` (id, user_id, bike_id, created_at, expires_at)
- `trips` (id, user_id, bike_id, start_station_id, end_station_id, start_time, end_time, duration_minutes, cost, status)
- `transactions` (id, trip_id, user_id, amount, razorpay_id, status, created_at)
- `refunds` (id, transaction_id, reason, amount, status, created_at)
- `support_tickets` (id, user_id, issue_type, description, status, created_at, resolved_at)

### **Booking Flow (Detailed)**
1. Customer opens app → sees map with stations and available bike counts (static, refreshed on demand)
2. Customer selects a bike → app reserves it for 5 minutes (prevents overbooking)
3. Customer walks to station, scans QR code with phone → trip starts, bike unlocks
4. Timer starts, customer can see running cost estimate based on current trip duration
5. Customer rides and returns bike to any station, locks it → trip ends automatically
6. Razorpay authorization (pre-authorized at signup) is charged for actual trip cost
7. Receipt is sent via email/SMS
8. If customer reports an issue within 24 hours, automatic refund is issued

### **Pricing Model**
- **Base fare:** ₹2 per trip
- **Per-minute rate:** ₹0.20 per minute
- **Threshold:** First 20 minutes included in base fare (no additional charge)
- **Formula:** Cost = 2 + max(0, (duration_minutes - 20) * 0.20)
- **Example:** 10-min trip = ₹2 | 30-min trip = ₹4

### **Payment Flow**
1. During signup, customer provides card details → Razorpay tokenizes and returns token
2. Token is stored securely in `payment_methods` table
3. At trip end, amount is charged using stored token
4. If charge fails, customer is notified and trip is marked as payment-pending
5. Refunds are issued within 24 hours for approved requests

### **API Contract (Key Endpoints)**
- `POST /auth/register` → Create user account
- `POST /auth/login` → Get JWT token
- `GET /map/nearby-bikes?lat=X&lng=Y` → Get bikes within 5 km
- `POST /bookings/reserve` → Reserve a bike (5-min lock)
- `POST /trips/start` → Start trip (QR code unlock)
- `POST /trips/end` → End trip (auto-charge)
- `GET /trips/history` → User's trip history
- `GET /admin/dashboard` → Admin overview
- `POST /admin/refund` → Process refund
- `GET /admin/analytics` → Revenue, utilization, trends

### **Bike QR Code System**
- Each bike has a unique QR code printed on it
- QR code contains hashed bike ID
- Customer scans → app sends hash to backend → backend verifies and unlocks bike
- No bike-specific hardware needed; works with any smartphone camera

### **Reservation Expiry & Overbooking Prevention**
- When customer reserves a bike, it's marked as "reserved" for 5 minutes
- If customer doesn't start trip within 5 minutes, reservation expires and bike becomes available
- Only one reservation per bike at a time

### **Support & Auto-Refund Policy**
- If customer reports an issue within 24 hours of trip completion, auto-refund is issued for 100% of trip cost
- For issues reported after 24 hours, support team reviews and decides on refund case-by-case
- Refund is issued to original payment method within 24-48 hours

### **Admin Authorization**
- Only users with `role=admin` in database can access admin endpoints
- Admin operations are logged for audit purposes

## Testing Decisions

### **What Makes a Good Test**
- Tests should verify **external behavior**, not implementation details
- Tests should be **deterministic** and not dependent on current time or randomness
- Tests should be **isolated** (mock external services like Razorpay, email providers)
- Tests should cover **happy path** and **edge cases** (e.g., expired reservations, failed payments)
- Tests should use **fixtures** for test data (users, bikes, stations, trips)

### **Modules to Test (Priority Order)**

#### **High Priority (Critical Logic)**
1. **Pricing & Billing Module**
   - Test trip cost calculation with various durations
   - Test discount code application
   - Test refund logic
   - Test edge cases (0-minute trip, 20-minute trip, 100-minute trip)

2. **Booking & Reservation Module**
   - Test bike reservation creation and expiry
   - Test trip start with valid/invalid QR codes
   - Test trip end and cost calculation
   - Test concurrent bookings (two users booking same bike)
   - Test expired reservation cleanup

3. **Geolocation & Map Module**
   - Test nearby bikes query with various coordinates
   - Test distance calculation accuracy
   - Test station availability aggregation
   - Test edge cases (duplicate bikes, inactive stations)

4. **Payment Processing Module**
   - Test payment authorization and charging (with Razorpay mock)
   - Test refund processing
   - Test payment failure handling
   - Test idempotency (duplicate charges should be prevented)

#### **Medium Priority (Important Logic)**
5. **Trip History & Analytics Module**
   - Test trip aggregation and filtering
   - Test utilization calculations
   - Test revenue aggregation by date/station
   - Test report generation

6. **Authentication & User Management Module**
   - Test user registration with valid/invalid email
   - Test login with correct/incorrect credentials
   - Test JWT token generation and validation
   - Test payment method storage

#### **Lower Priority (Integration/UI)**
7. **Admin & Operations Module** (integration tests only)
   - Test admin can create stations and bikes
   - Test admin can update pricing
   - Test admin can view analytics

8. **Notification & Support Module** (mock email/SMS providers)
   - Test email sent after trip completion
   - Test SMS OTP generation
   - Test support ticket creation

### **Test Framework & Tools**
- **Framework:** pytest (Python)
- **Async Testing:** pytest-asyncio for FastAPI async tests
- **Database:** pytest fixtures with temporary PostgreSQL database (or SQLite for speed)
- **Mocking:** unittest.mock for Razorpay, email, SMS providers
- **API Testing:** httpx for FastAPI testing
- **Fixtures:** Reusable test data (users, bikes, stations, trips)

### **Prior Art / Similar Tests in Codebase**
Since this is a new project, establish patterns for:
- Unit tests (test individual module logic)
- Integration tests (test module interactions with database)
- API tests (test HTTP endpoints end-to-end)

### **Test Coverage Goals**
- **Pricing Module:** 100% coverage (critical for revenue)
- **Booking Module:** 95% coverage (critical for functionality)
- **Geolocation Module:** 90% coverage
- **Payment Module:** 95% coverage (mock Razorpay)
- **Other Modules:** 70% coverage minimum

## Out of Scope

### **MVP Exclusions**
1. **Mobile App:** Web-first only; mobile can be built in v2
2. **Real-time Map Updates:** Static map with on-demand refresh; WebSocket can be added post-launch
3. **Surge Pricing:** Fixed pricing model for MVP; surge pricing logic in v2
4. **Insurance & Liability:** Assuming basic liability coverage is handled externally
5. **Bike Maintenance Workflow:** Admins manually mark bikes for maintenance; no automated detection
6. **Multi-city Support:** Single city only for MVP
7. **Integration with External APIs:** No real Razorpay integration needed for MVP testing (mock it)
8. **Premium Features:** Bike reservations with payment, loyalty points, rental plans (v2+)
9. **Advanced Analytics:** Heatmaps, demand prediction, ML-based pricing (v2+)
10. **Bike Tracking:** No GPS on bikes; QR code-based location only

### **Non-Functional Out of Scope**
1. **Load Testing & Performance Tuning:** Basic performance acceptable for MVP
2. **Security Hardening:** Basic auth/encryption; penetration testing in post-MVP
3. **Compliance:** GDPR, data retention policies (basic compliance only)
4. **Accessibility (WCAG):** Basic HTML best practices; full WCAG in v2

## Further Notes

### **Success Metrics**
- ✅ Users can book and complete a trip end-to-end without errors
- ✅ Admins can view dashboard, trips, and revenue metrics
- ✅ Payment integration works (mock Razorpay for MVP testing)
- ✅ All critical modules have >90% test coverage
- ✅ Platform can handle 100+ concurrent trips without crashing

### **Known Risks & Mitigation**
1. **Risk:** Bike theft or loss during free-floating period
   - **Mitigation:** QR code verification on unlock; honor system for MVP
2. **Risk:** Payment failures mid-trip
   - **Mitigation:** Pre-authorization at signup; graceful error handling; support team follows up
3. **Risk:** Bikes not returned to stations (abandoned bikes)
   - **Mitigation:** Trip timer continues; late fees accumulate; admin alerts after 1 hour
4. **Risk:** Station capacity exceeded during peak hours
   - **Mitigation:** Real-time availability updated; overflow handling (customers can lock at nearby station)

### **Future Enhancements (v2 & Beyond)**
- Mobile app (iOS/Android)
- Real-time WebSocket updates for live bike tracking
- Multi-city expansion
- Surge pricing and loyalty programs
- GPS tracking on bikes for anti-theft
- Integration with public transit APIs
- Bike maintenance automation
- Advanced analytics and demand forecasting
- Electric bike support
- Corporate accounts and B2B pricing

### **Development Timeline Estimate**
- **Phase 1 (Backend + Admin):** 3-4 weeks
  - Database schema, core modules, admin API
- **Phase 2 (Frontend + Payment):** 2-3 weeks
  - React web app, Razorpay integration, testing
- **Phase 3 (QA & Launch Prep):** 1-2 weeks
  - Testing, bug fixes, documentation
- **Total MVP Timeline:** 6-9 weeks

### **Deployment & DevOps**
- Docker containerization for easy deployment
- GitHub Actions for CI/CD (auto-run tests on push)
- Fly.io or Railway for hosting (automatic scaling)
- PostgreSQL managed database (PlanetScale or similar)
- Environment variables for config (API keys, database URLs)
- Health check endpoints for monitoring

