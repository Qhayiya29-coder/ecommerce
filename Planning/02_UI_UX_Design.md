# ExpressMarket - UI/UX Design Document

## 1. Design Principles

### 1.1 Core Principles
- **Simplicity**: Clean, uncluttered interface
- **Consistency**: Uniform design patterns across all pages
- **Accessibility**: WCAG 2.1 AA compliance
- **Responsiveness**: Mobile-first design approach
- **User-Centric**: Intuitive navigation and clear feedback

### 1.2 Design System
- **Framework**: Tailwind CSS 4.1
- **Color Palette**:
  - Primary: Blue (#2563eb) - Actions, links, highlights
  - Secondary: Gray (#6b7280) - Text, borders
  - Success: Green (#10b981) - Success messages
  - Warning: Yellow (#f59e0b) - Warnings
  - Error: Red (#ef4444) - Errors, delete actions
  - Background: White (#ffffff) - Main background
  - Surface: Gray-50 (#f9fafb) - Card backgrounds

- **Typography**:
  - Headings: Bold, various sizes (text-2xl, text-3xl)
  - Body: Regular, readable font sizes
  - Links: Blue, underlined on hover

- **Spacing**: Consistent padding and margins (4px, 8px, 16px, 24px, 32px)

## 2. Layout Structure

### 2.1 Global Navigation (Base Template)

**Header Structure:**
```
┌─────────────────────────────────────────────────────────────┐
│  ExpressMarket Logo    [Marketplace] [Cart] [My Orders]     │
│                              [Login] [Register] [Vendor]    │
└─────────────────────────────────────────────────────────────┘
```

**Navigation Rules:**
- **For Anonymous Users:**
  - Marketplace link
  - Login, Register, Become a Vendor links

- **For Authenticated Customers:**
  - Marketplace link
  - Cart (with item count badge)
  - My Orders link
  - Account, Logout links

- **For Authenticated Vendors:**
  - Marketplace link
  - Vendor Dashboard link
  - Account, Logout links
  - (Cart and Orders hidden)

**Footer:**
- Company information
- Links to important pages
- Copyright notice

### 2.2 Page Layouts

#### 2.2.1 Homepage (Product Listing)
```
┌─────────────────────────────────────────────────────────────┐
│  Breadcrumb: Home                                            │
│                                                               │
│  [Search Bar]  [Category Filter Dropdown]                    │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Product  │  │ Product  │  │ Product  │  │ Product  │   │
│  │  Image   │  │  Image   │  │  Image   │  │  Image   │   │
│  │  Name    │  │  Name    │  │  Name    │  │  Name    │   │
│  │  Price   │  │  Price   │  │  Price   │  │  Price   │   │
│  │ [Add to  │  │ [Add to  │  │ [Add to  │  │ [Add to  │   │
│  │  Cart]   │  │  Cart]   │  │  Cart]   │  │  Cart]   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                               │
│  [Pagination: Previous] [1] [2] [3] [Next]                    │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Grid layout (responsive: 1 col mobile, 2 cols tablet, 4 cols desktop)
- Product cards with image, name, price
- "Add to Cart" button (hidden for guests)
- Search functionality
- Category filtering
- Pagination

#### 2.2.2 Product Detail Page
```
┌─────────────────────────────────────────────────────────────┐
│  Breadcrumb: Home > Category > Product Name                  │
│                                                               │
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │              │  │  Product Name                      │  │
│  │   Product    │  │  Category: [Link]                  │  │
│  │    Image     │  │  Price: $XX.XX                     │  │
│  │              │  │  Rating: ★★★★☆ (4.5)              │  │
│  │              │  │                                    │  │
│  │              │  │  Sold by: Vendor Name              │  │
│  └──────────────┘  │                                    │  │
│                    │  Description:                      │  │
│                    │  [Product description text...]     │  │
│                    │                                    │  │
│                    │  Quantity: [1] [Add to Cart]       │  │
│                    └────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Customer Reviews                                      │  │
│  │  Average: 4.5 ★★★★☆ (25 reviews)                     │  │
│  │                                                        │  │
│  │  [Write Review Form - if purchased]                   │  │
│  │                                                        │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Username | ★★★★☆ | Date                      │  │  │
│  │  │  Review comment text...                        │  │  │
│  │  │  [Edit] [Delete]                               │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  │                                                        │  │
│  │  [Pagination]                                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  Related Products: [4 product cards]                         │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2.3 Shopping Cart Page
```
┌─────────────────────────────────────────────────────────────┐
│  Shopping Cart                                               │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Product Image | Product Name | Price | Qty | Total  │  │
│  │  [Remove]      |              | $XX   | [2]  | $XX   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Product Image | Product Name | Price | Qty | Total  │  │
│  │  [Remove]      |              | $XX   | [1]  | $XX   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  Subtotal: $XX.XX                                            │
│  Shipping: $0.00                                             │
│  ─────────────────                                           │
│  Total: $XX.XX                                               │
│                                                               │
│  [Continue Shopping]  [Proceed to Checkout]                  │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2.4 Checkout Page
```
┌─────────────────────────────────────────────────────────────┐
│  Checkout                                                    │
│                                                               │
│  ┌──────────────────────┐  ┌──────────────────────────┐  │
│  │  Order Summary        │  │  Shipping Information     │  │
│  │                       │  │                           │  │
│  │  Product 1 x 2        │  │  First Name: [_______]    │  │
│  │  Product 2 x 1        │  │  Last Name:  [_______]    │  │
│  │                       │  │  Email:      [_______]    │  │
│  │  Subtotal: $XX.XX     │  │  Phone:      [_______]    │  │
│  │  Shipping: $0.00      │  │                           │  │
│  │  ─────────────        │  │  Address:    [_______]    │  │
│  │  Total: $XX.XX        │  │  City:       [_______]    │  │
│  │                       │  │  Region:     [_______]    │  │
│  │                       │  │  Postal:     [_______]    │  │
│  │                       │  │  Country:    [Ethiopia]   │  │
│  │                       │  │                           │  │
│  │                       │  │  [Place Order]             │  │
│  └──────────────────────┘  └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2.5 Vendor Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  Vendor Dashboard                                            │
│                                                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Products │  │  Orders  │  │  Sales   │  │  Items   │  │
│  │    12    │  │    45    │  │  $1,234  │  │   156    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                               │
│  Store Status: [Active/Inactive] [Edit Store]                │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Recent Products                    [Add Product]     │  │
│  │  ┌────────┐ ┌────────┐ ┌────────┐                    │  │
│  │  │Product │ │Product │ │Product │                    │  │
│  │  │[Edit]  │ │[Edit]  │ │[Edit]  │                    │  │
│  │  └────────┘ └────────┘ └────────┘                    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Recent Orders                                        │  │
│  │  Order #12345 | Customer Name | $XX.XX | [View]     │  │
│  │  Order #12346 | Customer Name | $XX.XX | [View]     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 3. User Experience Flows

### 3.1 Customer Purchase Flow
```
Homepage → Product Detail → Add to Cart → Cart → Checkout → Order Confirmation
                                                              ↓
                                                         Email Sent
                                                              ↓
                                                         My Orders
```

### 3.2 Vendor Product Management Flow
```
Dashboard → Add Product → Product Form → Save → Product List
                                                      ↓
                                                 Edit/Delete
```

### 3.3 Review Submission Flow
```
Product Detail → (If Purchased) → Write Review Form → Submit → Review Displayed
```

## 4. Responsive Design Breakpoints

- **Mobile**: < 640px (1 column layout)
- **Tablet**: 640px - 1024px (2 column layout)
- **Desktop**: > 1024px (4 column layout)

## 5. Accessibility Features

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance (WCAG AA)
- Alt text for images
- Form labels and error messages
- Focus indicators

## 6. User Feedback Mechanisms

### 6.1 Success Messages
- Green background, checkmark icon
- Displayed at top of page
- Auto-dismiss after 5 seconds

### 6.2 Error Messages
- Red background, error icon
- Displayed near form fields
- Clear error descriptions

### 6.3 Loading States
- Spinner for async operations
- Disabled buttons during submission
- Progress indicators for long operations

## 7. Form Design Guidelines

- Clear labels above inputs
- Required field indicators (*)
- Inline validation feedback
- Error messages below fields
- Submit buttons at bottom
- Cancel/Back buttons for navigation
- Consistent input styling (rounded, padding, borders)

