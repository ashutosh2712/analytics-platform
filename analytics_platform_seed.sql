
-- ============================================
-- Analytics Platform Seed Data
-- ============================================

-- ORGANIZATION
INSERT INTO organizations (id, name)
VALUES
(1, 'Acme Analytics')
ON CONFLICT DO NOTHING;

-- USERS
-- Password for all users: secret123

INSERT INTO users (
    id,
    email,
    hashed_password,
    is_active
)
VALUES
(1,'owner@test.com','$2b$12$X5ZQ6W9i4Y9x7R4wD3m3quvB5B5n7fN8xQ1r6g9H7zD0J0vY7M4gG',true),
(2,'admin@test.com','$2b$12$X5ZQ6W9i4Y9x7R4wD3m3quvB5B5n7fN8xQ1r6g9H7zD0J0vY7M4gG',true),
(3,'analyst@test.com','$2b$12$X5ZQ6W9i4Y9x7R4wD3m3quvB5B5n7fN8xQ1r6g9H7zD0J0vY7M4gG',true),
(4,'viewer@test.com','$2b$12$X5ZQ6W9i4Y9x7R4wD3m3quvB5B5n7fN8xQ1r6g9H7zD0J0vY7M4gG',true)
ON CONFLICT DO NOTHING;

-- MEMBERSHIPS / RBAC
INSERT INTO memberships (
    id,
    user_id,
    organization_id,
    role
)
VALUES
(1,1,1,'OWNER'),
(2,2,1,'ADMIN'),
(3,3,1,'ANALYST'),
(4,4,1,'VIEWER')
ON CONFLICT DO NOTHING;

-- DASHBOARDS
INSERT INTO dashboards (
    id,
    name,
    organization_id
)
VALUES
(1,'Product Analytics Dashboard',1)
ON CONFLICT DO NOTHING;

-- WIDGETS
INSERT INTO widgets (
    id,
    dashboard_id,
    title,
    chart_type,
    metric
)
VALUES
(1,1,'Total Events','metric','count'),
(2,1,'Events Over Time','line','timeseries'),
(3,1,'Events By Name','bar','by_name')
ON CONFLICT DO NOTHING;

-- EVENTS
INSERT INTO events (
    organization_id,
    event_name,
    timestamp,
    properties
)
VALUES
(1, 'page_view', NOW() - INTERVAL '5 days', '{"page":"/home"}'),
(1, 'page_view', NOW() - INTERVAL '4 days', '{"page":"/pricing"}'),
(1, 'signup', NOW() - INTERVAL '4 days', '{"plan":"pro"}'),
(1, 'login', NOW() - INTERVAL '3 days', '{"device":"mobile"}'),
(1, 'purchase', NOW() - INTERVAL '3 days', '{"amount":99}'),
(1, 'purchase', NOW() - INTERVAL '2 days', '{"amount":149}'),
(1, 'page_view', NOW() - INTERVAL '2 days', '{"page":"/dashboard"}'),
(1, 'login', NOW() - INTERVAL '1 day', '{"device":"desktop"}'),
(1, 'signup', NOW() - INTERVAL '1 day', '{"plan":"enterprise"}'),
(1, 'page_view', NOW(), '{"page":"/reports"}');

-- Demo Accounts
-- Password for all accounts: secret123
-- OWNER   : owner@test.com
-- ADMIN   : admin@test.com
-- ANALYST : analyst@test.com
-- VIEWER  : viewer@test.com
