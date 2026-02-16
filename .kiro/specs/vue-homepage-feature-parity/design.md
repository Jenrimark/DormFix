# Design Document: Vue Homepage Feature Parity

## Overview

This design document outlines the implementation approach for achieving feature parity between the original HTML homepage and the Vue 3 version. The implementation will add missing sections (Core Features, enhanced Demo section, Footer) while maintaining the existing hero section and navigation structure.

## Architecture

### Component Structure

```
HomeView.vue (main container)
├── Hero Section (existing, minor updates)
├── Stats Grid (existing)
├── Core Features Section (NEW)
│   ├── Section Header
│   └── Role Cards Grid
│       ├── Student Role Card
│       ├── Admin Role Card
│       └── Technician Role Card
├── Demo Section (enhanced)
│   ├── Section Header (NEW)
│   └── Demo Cards Grid (existing, enhanced)
└── Footer Component (NEW)

AppNav.vue (navigation)
├── Logo & Brand
├── Anchor Links (NEW)
│   ├── Features Link
│   └── Demo Link
└── CTA Button (existing)
```

### Design Decisions

1. **Single File Component**: Keep all new sections within HomeView.vue rather than creating separate components, as the content is static and specific to the homepage
2. **SVG Icons**: Use inline SVG instead of emoji for professional appearance and better accessibility
3. **Smooth Scrolling**: Implement anchor-based navigation with smooth scroll behavior
4. **Tailwind Classes**: Maintain consistency with existing codebase by using Tailwind utility classes

## Components and Interfaces

### HomeView.vue Enhancements

**New Template Sections:**

```vue
<!-- Core Features Section -->
<section id="features" class="bg-white py-20">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Section header with title and subtitle -->
    <!-- Grid of 3 role cards (Student, Admin, Technician) -->
    <!-- Each card contains: icon, title, feature list with checkmarks -->
  </div>
</section>

<!-- Enhanced Demo Section -->
<section id="demo" class="py-20">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Section header (NEW) -->
    <!-- Existing demo cards grid with enhanced styling -->
  </div>
</section>

<!-- Footer Component -->
<footer class="bg-white border-t border-gray-200 py-8">
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600">
    <!-- Project name and copyright -->
  </div>
</footer>
```

**Script Section:**

```javascript
<script setup>
// No reactive state needed - all content is static
// Smooth scroll behavior handled by CSS
</script>
```

**Style Section:**

```vue
<style scoped>
/* Smooth scroll behavior for anchor links */
html {
  scroll-behavior: smooth;
}
</style>
```

### AppNav.vue Enhancements

**New Navigation Links:**

```vue
<template>
  <nav>
    <!-- Existing logo and brand -->
    <div class="flex items-center space-x-4">
      <!-- NEW: Anchor links -->
      <a href="#features" class="text-gray-600 hover:text-primary transition-colors duration-200">
        功能
      </a>
      <a href="#demo" class="text-gray-600 hover:text-primary transition-colors duration-200">
        演示
      </a>
      <!-- Existing CTA button -->
    </div>
  </nav>
</template>
```

## Data Models

### Role Card Data Structure

```javascript
// JavaScript object structure for role cards
const roleCard = {
  id: '',              // 'student' | 'admin' | 'technician'
  icon: '',            // SVG path data
  iconBgColor: '',     // Tailwind class for icon background
  iconColor: '',       // Tailwind class for icon color
  title: '',           // Role name in Chinese
  features: []         // Array of 4 feature descriptions
}
```

### Feature List Data

```javascript
const roleCards = [
  {
    id: 'student',
    icon: '<path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>',
    iconBgColor: 'bg-primary/10',
    iconColor: 'text-primary',
    title: '学生端',
    features: [
      '在线提交报修申请',
      '实时跟踪工单状态',
      '上传现场照片',
      '评价维修服务'
    ]
  },
  {
    id: 'admin',
    icon: '<path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>',
    iconBgColor: 'bg-cta/10',
    iconColor: 'text-cta',
    title: '管理员端',
    features: [
      '数据可视化仪表盘',
      '智能派单系统',
      '工单审核管理',
      '统计报表导出'
    ]
  },
  {
    id: 'technician',
    icon: '<path d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>',
    iconBgColor: 'bg-blue-100',
    iconColor: 'text-blue-600',
    title: '维修员端',
    features: [
      '接收派单通知',
      '更新维修进度',
      '查看工单详情',
      '填写维修备注'
    ]
  }
];
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Role Card Structure Completeness

*For any* render of the Features section, it should contain exactly 3 role cards, and each role card should have a non-empty title, an SVG icon element, and exactly 4 feature list items.

**Validates: Requirements 1.2, 1.3**

### Property 2: SVG Icon Usage

*For any* icon element in role cards, it should be rendered as an inline SVG element (not emoji or image tag) with proper viewBox attribute.

**Validates: Requirements 1.4**

### Property 3: Feature List Checkmark Icons

*For any* feature list item in role cards, it should contain a green checkmark SVG icon with the correct path data.

**Validates: Requirements 5.3**

### Property 4: Hover State Visual Feedback

*For any* interactive card element (role cards or demo cards), the element should have hover state CSS classes that modify shadow, border, or background properties.

**Validates: Requirements 1.5, 3.3, 2.3**

### Property 5: Responsive Grid Layout

*For any* viewport width, the Features section grid should use grid-cols-1 class at widths <768px and md:grid-cols-3 class at widths ≥768px.

**Validates: Requirements 6.1, 6.2**

### Property 6: Color Theme Consistency

*For any* element using theme colors, it should use Tailwind classes that map to the defined color values (bg-primary, text-primary, bg-cta, text-cta) rather than arbitrary color values.

**Validates: Requirements 5.1**

### Property 7: Typography Class Usage

*For any* heading element, it should use font-heading class, and any body text should use font-body class or inherit from parent.

**Validates: Requirements 5.2**

### Property 8: Footer Styling

*For any* render of the Footer, it should have a white background class (bg-white) and a top border class (border-t).

**Validates: Requirements 4.4**

## Error Handling

### Missing Section IDs

**Scenario**: User clicks anchor link but target section ID doesn't exist

**Handling**: 
- Browser default behavior (no scroll)
- No error thrown
- Navigation link remains functional

### Invalid SVG Path Data

**Scenario**: SVG path data is malformed or empty

**Handling**:
- Icon container still renders with background color
- Empty space where icon should be
- Card layout remains intact

### Responsive Breakpoint Edge Cases

**Scenario**: Viewport width exactly at breakpoint (768px)

**Handling**:
- Tailwind's `md:` prefix applies at ≥768px
- Consistent behavior across browsers
- No layout shift or flicker

## Testing Strategy

### Unit Tests

**Test File**: `HomeView.test.js`

1. **Section Presence Tests**
   - Verify all section IDs exist (#features, #demo)
   - Verify Footer component renders
   - Verify section headers display correct text

2. **Role Card Rendering Tests**
   - Verify 3 role cards render
   - Verify each card has 4 feature items
   - Verify SVG icons render with correct viewBox

3. **Navigation Link Tests**
   - Verify anchor links have correct href attributes
   - Verify hover classes apply correctly

### Property-Based Tests

**Test File**: `HomeView.property.test.js`

**Framework**: Vitest with fast-check library (JavaScript)

**Configuration**: Minimum 100 iterations per property test

1. **Property Test: Section Rendering Completeness**
   - Generate random page mount scenarios
   - Verify all sections present in DOM
   - **Tag**: Feature: vue-homepage-feature-parity, Property 1: Section Rendering Completeness

2. **Property Test: Role Card Data Integrity**
   - Generate role card data variations
   - Verify structure matches interface
   - **Tag**: Feature: vue-homepage-feature-parity, Property 2: Role Card Data Integrity

3. **Property Test: Responsive Layout Adaptation**
   - Generate random viewport widths
   - Verify grid column count matches breakpoint rules
   - **Tag**: Feature: vue-homepage-feature-parity, Property 5: Responsive Layout Adaptation

### Integration Tests

1. **Anchor Navigation Flow**
   - Click "功能" link → verify scroll to #features
   - Click "演示" link → verify scroll to #demo
   - Verify smooth scroll behavior

2. **Visual Regression Tests**
   - Compare rendered output with HTML version screenshots
   - Verify spacing, colors, typography match

### Manual Testing Checklist

- [ ] Test on Chrome, Firefox, Safari
- [ ] Test on mobile (375px), tablet (768px), desktop (1440px)
- [ ] Verify all hover states work
- [ ] Verify smooth scrolling works
- [ ] Compare side-by-side with HTML version
- [ ] Verify accessibility (keyboard navigation, screen reader)
