# How to Add Your Logo

## Current Setup

The app currently has a WiFi icon (🔔) as a placeholder logo in the header toolbar.

## Option 1: Use Your Own Logo Image

### Step 1: Add Your Logo File

1. Place your logo file in: `src/assets/images/`
2. Supported formats: PNG, JPG, SVG (SVG recommended for best quality)
3. Recommended size: 200x200 pixels or similar square/rectangular ratio

```
ionic-app/
└── src/
    └── assets/
        └── images/
            └── logo.png  ← Your logo here
```

### Step 2: Update the HTML

Edit `src/app/home/home.page.html`:

Replace this:
```html
<div class="logo-container">
  <ion-icon name="wifi" class="logo-icon"></ion-icon>
</div>
```

With this:
```html
<div class="logo-container">
  <img src="assets/images/logo.png" alt="Company Logo" class="logo-image">
</div>
```

## Option 2: Change the Icon

You can use any Ionicon instead of "wifi". Browse icons at: https://ionic.io/ionicons

Popular telecom icons:
- `wifi` - WiFi symbol
- `globe` - Globe/network
- `radio` - Radio waves
- `cellular` - Cell signal
- `call` - Phone
- `business` - Building

To change, edit `src/app/home/home.page.html`:
```html
<ion-icon name="cellular" class="logo-icon"></ion-icon>
```

## Option 3: Add Text Logo

Edit `src/app/home/home.page.html`:
```html
<div class="logo-container">
  <span class="text-logo">Frontier</span>
</div>
```

Add to `src/app/home/home.page.scss`:
```scss
.logo-container {
  .text-logo {
    font-size: 20px;
    font-weight: bold;
    color: var(--ion-color-primary);
    letter-spacing: 1px;
  }
}
```

## Option 4: Add Both Icon and Text

```html
<div class="logo-container">
  <ion-icon name="wifi" class="logo-icon"></ion-icon>
  <span class="logo-text">Frontier</span>
</div>
```

Add to CSS:
```scss
.logo-container {
  gap: 8px; // Space between icon and text
  
  .logo-text {
    font-size: 18px;
    font-weight: 600;
    color: var(--ion-color-primary);
  }
}
```

## Styling Tips

### Adjust Logo Size

In `src/app/home/home.page.scss`:

```scss
.logo-container {
  img.logo-image {
    height: 50px;  // Change this value
    width: auto;
  }
}
```

### Change Logo Color (for icons)

```scss
.logo-icon {
  font-size: 32px;
  color: #8B0000;  // Your custom color
}
```

### Add Logo Animation (Optional)

```scss
.logo-icon {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}
```

## Preview Your Changes

After making changes, the app will automatically reload. If not:
- Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
- Or restart: `ionic serve`

## Troubleshooting

**Logo not showing?**
1. Check file path: `src/assets/images/logo.png`
2. Make sure assets folder exists
3. Check browser console for errors (F12)

**Logo too big/small?**
- Adjust the `height` value in the CSS

**Wrong color?**
- Change the `color` property in `.logo-icon` or `.logo-image`

## Current Logo Location

The logo appears in the **top-left** of the toolbar header, visible on all pages.

---

**Need help?** Check the [Ionic Documentation](https://ionicframework.com/docs) for more customization options!
