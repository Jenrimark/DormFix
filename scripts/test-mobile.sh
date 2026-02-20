#!/bin/bash

# Mobile Testing Script for DormFix Homepage
# This script helps automate mobile testing checks

set -e

echo "🧪 DormFix Mobile Testing Script"
echo "================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if frontend dev server is running
echo "📡 Checking if frontend dev server is running..."
if curl -s http://localhost:5173 > /dev/null; then
    echo -e "${GREEN}✓${NC} Frontend dev server is running"
else
    echo -e "${RED}✗${NC} Frontend dev server is not running"
    echo "   Please start it with: cd frontend-vue && npm run dev"
    exit 1
fi

echo ""
echo "📱 Mobile Testing Checklist"
echo "============================"
echo ""

# Get local IP address
echo "🌐 Network Information:"
echo "   Local URL: http://localhost:5173"
if command -v ifconfig &> /dev/null; then
    LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
    if [ ! -z "$LOCAL_IP" ]; then
        echo "   Network URL: http://$LOCAL_IP:5173"
        echo "   Use this URL to test on real mobile devices on the same network"
    fi
fi

echo ""
echo "🔍 Testing Instructions:"
echo ""
echo "1. Browser DevTools Simulation:"
echo "   - Open Chrome: http://localhost:5173"
echo "   - Press F12 to open DevTools"
echo "   - Press Ctrl+Shift+M (Cmd+Shift+M on Mac) for device toolbar"
echo "   - Test these device presets:"
echo "     • iPhone SE (375x667)"
echo "     • iPhone 12/13/14 (390x844)"
echo "     • Pixel 5 (393x851)"
echo "     • iPad (768x1024)"
echo ""

echo "2. Real Device Testing (iOS):"
echo "   - Connect iPhone to same WiFi network"
if [ ! -z "$LOCAL_IP" ]; then
    echo "   - Open Safari and navigate to: http://$LOCAL_IP:5173"
else
    echo "   - Open Safari and navigate to: http://[YOUR_IP]:5173"
fi
echo "   - Test all interactions and features"
echo ""

echo "3. Real Device Testing (Android):"
echo "   - Connect Android device to same WiFi network"
if [ ! -z "$LOCAL_IP" ]; then
    echo "   - Open Chrome and navigate to: http://$LOCAL_IP:5173"
else
    echo "   - Open Chrome and navigate to: http://[YOUR_IP]:5173"
fi
echo "   - Test all interactions and features"
echo ""

echo "📋 Test Cases to Verify:"
echo ""
echo "  Layout & Responsiveness:"
echo "  [ ] Hero section is full-screen"
echo "  [ ] Stats cards in 1 column on mobile (375px)"
echo "  [ ] Stats cards in 3 columns on tablet (768px)"
echo "  [ ] Features cards adapt to screen size"
echo "  [ ] No horizontal scroll"
echo "  [ ] Typography is readable (≥16px)"
echo ""

echo "  Visual Effects:"
echo "  [ ] Gradient text renders (purple to cyan)"
echo "  [ ] Animated floating blobs work smoothly"
echo "  [ ] Glassmorphism cards have backdrop-blur"
echo "  [ ] Hover effects work (or adapt for touch)"
echo "  [ ] Smooth transitions"
echo ""

echo "  Touch Interactions:"
echo "  [ ] '立即报修' button navigates to /submit-order"
echo "  [ ] '查看工单' button navigates to /order-tracking"
echo "  [ ] Quick start cards are tappable"
echo "  [ ] All touch targets ≥44x44px"
echo "  [ ] No double-tap delay"
echo ""

echo "  Performance:"
echo "  [ ] Page loads in <3 seconds on Fast 3G"
echo "  [ ] Smooth scrolling (60fps)"
echo "  [ ] Animations don't cause jank"
echo "  [ ] No memory leaks"
echo ""

echo "  Accessibility:"
echo "  [ ] Text contrast meets WCAG AA (≥4.5:1)"
echo "  [ ] Touch targets are adequately sized"
echo "  [ ] Reduced motion is respected"
echo "  [ ] No content overflow"
echo ""

echo "  iOS Safari Specific:"
echo "  [ ] -webkit-backdrop-filter works"
echo "  [ ] Gradient text renders correctly"
echo "  [ ] No 100vh viewport issues"
echo "  [ ] Touch interactions work"
echo ""

echo "  Android Chrome Specific:"
echo "  [ ] backdrop-filter works"
echo "  [ ] Gradient text renders correctly"
echo "  [ ] Address bar behavior is acceptable"
echo "  [ ] Touch interactions work"
echo ""

echo "📊 Performance Testing:"
echo ""
echo "  To test performance in Chrome DevTools:"
echo "  1. Open DevTools (F12)"
echo "  2. Go to Lighthouse tab"
echo "  3. Select 'Mobile' device"
echo "  4. Select 'Performance' category"
echo "  5. Click 'Analyze page load'"
echo "  6. Verify scores:"
echo "     • Performance: ≥90"
echo "     • Accessibility: ≥90"
echo "     • Best Practices: ≥90"
echo ""

echo "🐛 Common Issues to Check:"
echo ""
echo "  iOS Safari:"
echo "  - backdrop-filter may need -webkit prefix"
echo "  - 100vh includes address bar (use min-h-screen)"
echo "  - Gradient text may have rendering issues"
echo ""
echo "  Android Chrome:"
echo "  - Address bar hides on scroll (test layout)"
echo "  - backdrop-filter support varies by version"
echo "  - Touch feedback may need explicit styling"
echo ""

echo "📝 Documentation:"
echo ""
echo "  Full testing guide: README/mobile-testing-guide.md"
echo "  Design document: .kiro/specs/vue-homepage-redesign/design.md"
echo "  Tasks document: .kiro/specs/vue-homepage-redesign/tasks.md"
echo ""

echo "✅ Testing script complete!"
echo ""
echo "Next steps:"
echo "1. Follow the testing instructions above"
echo "2. Document results in README/mobile-testing-guide.md"
echo "3. Fix any issues found"
echo "4. Re-test after fixes"
echo "5. Mark task 16.3 as complete in tasks.md"
echo ""
