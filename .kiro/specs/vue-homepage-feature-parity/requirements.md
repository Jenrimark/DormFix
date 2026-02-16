# Requirements Document

## Introduction

This specification defines the requirements for achieving feature parity between the original HTML homepage and the Vue 3 version homepage for the DormFix dormitory repair system. The Vue version is currently missing several key sections that provide important information to users about system capabilities and role-specific features.

## Glossary

- **HomeView**: The Vue 3 component that renders the main landing page
- **Feature_Section**: A dedicated section showcasing role-specific system capabilities
- **Role_Card**: A visual card component displaying features for a specific user role (Student, Admin, Technician)
- **Demo_Section**: A section providing quick access links to different system interfaces
- **Footer**: The bottom section of the page containing project information and copyright

## Requirements

### Requirement 1: Core Features Section

**User Story:** As a visitor, I want to see detailed information about system capabilities for each user role, so that I can understand what features are available before using the system.

#### Acceptance Criteria

1. WHEN the homepage loads, THE HomeView SHALL display a "核心功能" (Core Features) section after the hero area
2. THE Feature_Section SHALL contain three Role_Cards for Student, Admin, and Technician roles
3. WHEN displaying each Role_Card, THE HomeView SHALL show a role-specific icon, title, and list of 4 features
4. THE Feature_Section SHALL use SVG icons instead of emoji for professional appearance
5. WHEN a user hovers over a Role_Card, THE HomeView SHALL provide visual feedback with shadow transition

### Requirement 2: Navigation Anchor Links

**User Story:** As a visitor, I want to quickly navigate to different sections of the homepage, so that I can find information efficiently.

#### Acceptance Criteria

1. THE AppNav component SHALL include anchor links for "功能" (Features) and "演示" (Demo) sections
2. WHEN a user clicks an anchor link, THE HomeView SHALL smoothly scroll to the corresponding section
3. THE navigation links SHALL highlight on hover with color transition

### Requirement 3: Demo Section Enhancement

**User Story:** As a visitor, I want clear visual distinction between different demo entry points, so that I can easily identify which interface to explore.

#### Acceptance Criteria

1. THE Demo_Section SHALL display three demo cards with descriptive titles and explanations
2. WHEN displaying demo cards, THE HomeView SHALL use consistent emoji icons (📝, 📊, 🔍)
3. WHEN a user hovers over a demo card, THE HomeView SHALL change the border color to match the role theme
4. THE Demo_Section SHALL include a section header "在线演示" (Online Demo) with subtitle

### Requirement 4: Footer Component

**User Story:** As a visitor, I want to see project information and copyright details, so that I understand the context and ownership of the system.

#### Acceptance Criteria

1. THE HomeView SHALL display a Footer component at the bottom of the page
2. THE Footer SHALL contain the project name "DormFix - 基于 Django 的宿舍报修工单系统"
3. THE Footer SHALL display copyright text "软件工程专业毕业设计项目 © 2026"
4. THE Footer SHALL use a white background with top border for visual separation

### Requirement 5: Visual Consistency

**User Story:** As a visitor, I want the Vue version to match the visual design of the original HTML version, so that the user experience is consistent.

#### Acceptance Criteria

1. THE HomeView SHALL use the same color scheme as the HTML version (primary: #7C3AED, cta: #F97316)
2. THE HomeView SHALL use the same typography (Fira Code for headings, Fira Sans for body)
3. WHEN displaying feature lists, THE HomeView SHALL use green checkmark SVG icons
4. THE HomeView SHALL maintain the same spacing and layout structure as the HTML version
5. THE HomeView SHALL use Tailwind CSS classes consistent with the original design

### Requirement 6: Responsive Layout

**User Story:** As a mobile user, I want the enhanced homepage to display properly on small screens, so that I can access information on any device.

#### Acceptance Criteria

1. WHEN viewed on mobile devices, THE Feature_Section SHALL stack Role_Cards vertically
2. WHEN viewed on tablet devices (≥768px), THE Feature_Section SHALL display Role_Cards in a 3-column grid
3. THE Demo_Section SHALL maintain responsive behavior across all screen sizes
4. THE Footer SHALL remain readable and properly formatted on mobile devices
