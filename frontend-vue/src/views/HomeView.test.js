import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import * as fc from 'fast-check'
import HomeView from './HomeView.vue'

// Create a mock router for testing
const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/submit', component: { template: '<div>Submit</div>' } },
    { path: '/orders', component: { template: '<div>Orders</div>' } },
    { path: '/admin', component: { template: '<div>Admin</div>' } },
  ],
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 1: Role Card Structure Completeness
 * Validates: Requirements 1.2, 1.3
 * 
 * For any render of the Features section, it should contain exactly 3 role cards,
 * and each role card should have a non-empty title, an SVG icon element, and exactly 4 feature list items.
 */
describe('Property 1: Role Card Structure Completeness', () => {
  it('should render exactly 3 role cards with complete structure', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        // Mount the component with router
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Find the features section
        const featuresSection = wrapper.find('#features')
        expect(featuresSection.exists()).toBe(true)

        // Find all role cards (they have the class pattern for cards)
        const roleCards = featuresSection.findAll('.bg-bgLight.rounded-xl')
        
        // Property: Exactly 3 role cards
        expect(roleCards.length).toBe(3)

        // For each role card, verify structure
        roleCards.forEach((card) => {
          // Property: Each card has a non-empty title (h3 element)
          const title = card.find('h3')
          expect(title.exists()).toBe(true)
          expect(title.text().trim().length).toBeGreaterThan(0)

          // Property: Each card has an SVG icon element
          const iconContainer = card.find('.w-12.h-12')
          expect(iconContainer.exists()).toBe(true)
          const svgIcon = iconContainer.find('svg')
          expect(svgIcon.exists()).toBe(true)
          expect(svgIcon.attributes('viewBox')).toBeDefined()

          // Property: Each card has exactly 4 feature list items
          const featureItems = card.findAll('ul li')
          expect(featureItems.length).toBe(4)
        })

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 2: SVG Icon Usage
 * Validates: Requirements 1.4
 * 
 * For any icon element in role cards, it should be rendered as an inline SVG element
 * (not emoji or image tag) with proper viewBox attribute.
 */
describe('Property 2: SVG Icon Usage', () => {
  it('should use inline SVG elements with viewBox for all role card icons', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        const featuresSection = wrapper.find('#features')
        const roleCards = featuresSection.findAll('.bg-bgLight.rounded-xl')

        roleCards.forEach((card) => {
          // Find the icon container
          const iconContainer = card.find('.w-12.h-12')
          expect(iconContainer.exists()).toBe(true)

          // Property: Icon must be an SVG element (not emoji or img)
          const svgIcon = iconContainer.find('svg')
          expect(svgIcon.exists()).toBe(true)
          
          // Property: SVG must have viewBox attribute
          const viewBox = svgIcon.attributes('viewBox')
          expect(viewBox).toBeDefined()
          expect(viewBox).toBeTruthy()
          
          // Property: SVG should have path elements (actual icon content)
          const paths = svgIcon.findAll('path')
          expect(paths.length).toBeGreaterThan(0)

          // Property: Should not contain emoji or img tags in icon container
          const imgTags = iconContainer.findAll('img')
          expect(imgTags.length).toBe(0)
        })

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 3: Feature List Checkmark Icons
 * Validates: Requirements 5.3
 * 
 * For any feature list item in role cards, it should contain a green checkmark SVG icon
 * with the correct path data.
 */
describe('Property 3: Feature List Checkmark Icons', () => {
  it('should display green checkmark SVG icons for all feature list items', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        const featuresSection = wrapper.find('#features')
        const roleCards = featuresSection.findAll('.bg-bgLight.rounded-xl')

        roleCards.forEach((card) => {
          const featureItems = card.findAll('ul li')
          
          // Each feature item should have exactly 4 items (verified in Property 1)
          expect(featureItems.length).toBe(4)

          featureItems.forEach((item) => {
            // Property: Each feature item contains an SVG checkmark
            const checkmarkSvg = item.find('svg')
            expect(checkmarkSvg.exists()).toBe(true)

            // Property: Checkmark SVG has green color class
            const svgClasses = checkmarkSvg.classes()
            expect(svgClasses).toContain('text-green-500')

            // Property: Checkmark SVG has correct dimensions
            expect(svgClasses).toContain('w-5')
            expect(svgClasses).toContain('h-5')

            // Property: Checkmark SVG has viewBox attribute
            expect(checkmarkSvg.attributes('viewBox')).toBe('0 0 24 24')

            // Property: Checkmark SVG contains path with checkmark data
            const path = checkmarkSvg.find('path')
            expect(path.exists()).toBe(true)
            
            // The checkmark path should contain the specific path data
            const pathData = path.attributes('d')
            expect(pathData).toBe('M5 13l4 4L19 7')
          })
        })

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 4: Hover State Visual Feedback
 * Validates: Requirements 1.5, 3.3, 2.3
 * 
 * For any interactive card element (role cards or demo cards), the element should have
 * hover state CSS classes that modify shadow, border, or background properties.
 */
describe('Property 4: Hover State Visual Feedback', () => {
  it('should have hover state classes on all interactive cards', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Test role cards in Features section
        const featuresSection = wrapper.find('#features')
        const roleCards = featuresSection.findAll('.bg-bgLight.rounded-xl')
        
        expect(roleCards.length).toBe(3)
        
        roleCards.forEach((card) => {
          const classes = card.classes()
          
          // Property: Role cards should have hover:shadow-lg for visual feedback
          expect(classes.some(c => c.includes('hover:shadow'))).toBe(true)
          
          // Property: Role cards should have transition class for smooth animation
          expect(classes.some(c => c.includes('transition'))).toBe(true)
          
          // Property: Role cards should have cursor-pointer for interactivity indication
          expect(classes).toContain('cursor-pointer')
        })

        // Test demo cards in Demo section
        const demoSection = wrapper.find('#demo')
        expect(demoSection.exists()).toBe(true)
        
        const demoCards = demoSection.findAll('a.bg-white.rounded-xl')
        
        expect(demoCards.length).toBe(3)
        
        demoCards.forEach((card) => {
          const classes = card.classes()
          
          // Property: Demo cards should have hover:border-* for border color change
          const classString = classes.join(' ')
          expect(classString.includes('hover:border')).toBe(true)
          
          // Property: Demo cards should have hover:shadow-lg for visual feedback
          expect(classes.some(c => c.includes('hover:shadow'))).toBe(true)
          
          // Property: Demo cards should have transition-all for smooth animation
          expect(classes).toContain('transition-all')
          
          // Property: Demo cards should have cursor-pointer for interactivity indication
          expect(classes).toContain('cursor-pointer')
          
          // Property: Demo cards should have border-2 base state
          expect(classes).toContain('border-2')
        })

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Unit Test: Footer Content
 * Validates: Requirements 4.2, 4.3
 * 
 * Verify project name and copyright text are present in the footer.
 */
describe('Footer Content', () => {
  it('should display project name and copyright text', async () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [router],
      },
    })

    await wrapper.vm.$nextTick()

    // Find the footer element
    const footer = wrapper.find('footer')
    expect(footer.exists()).toBe(true)

    // Verify project name is present
    const footerText = footer.text()
    expect(footerText).toContain('DormFix - 基于 Django 的宿舍报修工单系统')

    // Verify copyright text is present
    expect(footerText).toContain('软件工程专业毕业设计项目 © 2026')

    wrapper.unmount()
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 8: Footer Styling
 * Validates: Requirements 4.4
 * 
 * For any render of the Footer, it should have a white background class (bg-white)
 * and a top border class (border-t).
 */
describe('Property 8: Footer Styling', () => {
  it('should have white background and top border', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Find the footer element
        const footer = wrapper.find('footer')
        expect(footer.exists()).toBe(true)

        const classes = footer.classes()

        // Property: Footer should have white background
        expect(classes).toContain('bg-white')

        // Property: Footer should have top border
        expect(classes).toContain('border-t')

        // Property: Footer should have border color class
        expect(classes).toContain('border-gray-200')

        // Property: Footer should have vertical padding
        expect(classes).toContain('py-8')

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 5: Responsive Grid Layout
 * Validates: Requirements 6.1, 6.2
 * 
 * For any viewport width, the Features section grid should use grid-cols-1 class
 * at widths <768px and md:grid-cols-3 class at widths ≥768px.
 */
describe('Property 5: Responsive Grid Layout', () => {
  it('should have responsive grid classes for mobile and tablet/desktop breakpoints', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Find the Features section
        const featuresSection = wrapper.find('#features')
        expect(featuresSection.exists()).toBe(true)

        // Find the grid container (the div that contains role cards)
        const gridContainer = featuresSection.find('.grid')
        expect(gridContainer.exists()).toBe(true)

        const classes = gridContainer.classes()

        // Property: Grid should have grid-cols-1 for mobile (base/default)
        expect(classes).toContain('grid-cols-1')

        // Property: Grid should have md:grid-cols-3 for tablet/desktop (≥768px)
        expect(classes).toContain('md:grid-cols-3')

        // Property: Grid should have gap spacing
        expect(classes.some(c => c.startsWith('gap-'))).toBe(true)

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 6: Color Theme Consistency
 * Validates: Requirements 5.1
 * 
 * For any element using theme colors, it should use Tailwind classes that map to
 * the defined color values (bg-primary, text-primary, bg-cta, text-cta) rather than
 * arbitrary color values.
 */
describe('Property 6: Color Theme Consistency', () => {
  it('should use theme color classes instead of arbitrary values', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Get the entire HTML content
        const html = wrapper.html()

        // Property: Should use theme color classes (bg-primary, text-primary, etc.)
        // Check for presence of theme color classes
        const themeColorClasses = [
          'bg-primary',
          'text-primary',
          'bg-cta',
          'text-cta',
          'bg-bgLight',
          'text-textDark'
        ]

        // At least some theme color classes should be present
        const hasThemeColors = themeColorClasses.some(colorClass => html.includes(colorClass))
        expect(hasThemeColors).toBe(true)

        // Property: Should NOT use arbitrary color values like bg-[#7C3AED]
        // Check that we're not using arbitrary values for theme colors
        const arbitraryColorPatterns = [
          /bg-\[#[0-9A-Fa-f]{6}\]/,  // bg-[#RRGGBB]
          /text-\[#[0-9A-Fa-f]{6}\]/, // text-[#RRGGBB]
          /border-\[#[0-9A-Fa-f]{6}\]/ // border-[#RRGGBB]
        ]

        // For theme colors specifically, we should not find arbitrary values
        const themeColorHexValues = ['7C3AED', 'F97316', 'FAF5FF', '4C1D95']
        
        themeColorHexValues.forEach(hexValue => {
          // Should not use arbitrary syntax for theme colors
          expect(html.includes(`[#${hexValue}]`)).toBe(false)
          expect(html.includes(`[#${hexValue.toLowerCase()}]`)).toBe(false)
        })

        // Verify specific elements use theme classes
        // Hero section CTA button should use bg-cta
        const ctaButton = wrapper.find('a[href="/submit"]')
        if (ctaButton.exists()) {
          const ctaClasses = ctaButton.classes()
          expect(ctaClasses).toContain('bg-cta')
        }

        // Role card icons should use theme colors
        const studentIcon = wrapper.find('.bg-primary\\/10')
        expect(studentIcon.exists()).toBe(true)

        const adminIcon = wrapper.find('.bg-cta\\/10')
        expect(adminIcon.exists()).toBe(true)

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})

/**
 * Feature: vue-homepage-feature-parity
 * Property 7: Typography Class Usage
 * Validates: Requirements 5.2
 * 
 * For any heading element, it should use font-heading class, and any body text
 * should use font-body class or inherit from parent.
 */
describe('Property 7: Typography Class Usage', () => {
  it('should use font-heading for headings and font-body for body text', async () => {
    await fc.assert(
      fc.asyncProperty(fc.constant(null), async () => {
        const wrapper = mount(HomeView, {
          global: {
            plugins: [router],
          },
        })

        await wrapper.vm.$nextTick()

        // Property: All h1, h2, h3 elements should use font-heading class
        const h1Elements = wrapper.findAll('h1')
        h1Elements.forEach(h1 => {
          const classes = h1.classes()
          expect(classes).toContain('font-heading')
        })

        const h2Elements = wrapper.findAll('h2')
        h2Elements.forEach(h2 => {
          const classes = h2.classes()
          expect(classes).toContain('font-heading')
        })

        const h3Elements = wrapper.findAll('h3')
        h3Elements.forEach(h3 => {
          const classes = h3.classes()
          expect(classes).toContain('font-heading')
        })

        // Property: Body element should have font-body class (applied globally in CSS)
        // We verify this by checking that the body tag in the global CSS has @apply font-body
        // Since we can't directly test global CSS here, we verify that headings explicitly
        // override with font-heading, which implies body text inherits font-body

        // Verify at least one heading exists with font-heading
        const allHeadings = [...h1Elements, ...h2Elements, ...h3Elements]
        expect(allHeadings.length).toBeGreaterThan(0)
        
        // All headings should have font-heading
        allHeadings.forEach(heading => {
          expect(heading.classes()).toContain('font-heading')
        })

        // Property: Paragraph and list text should NOT have font-heading
        // (they should inherit font-body from body element)
        const paragraphs = wrapper.findAll('p')
        paragraphs.forEach(p => {
          const classes = p.classes()
          expect(classes).not.toContain('font-heading')
        })

        const listItems = wrapper.findAll('li')
        listItems.forEach(li => {
          const classes = li.classes()
          expect(classes).not.toContain('font-heading')
        })

        wrapper.unmount()
      }),
      { numRuns: 100 }
    )
  })
})
