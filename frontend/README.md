# Fewfinder Frontend

A modern React application for searching YouTube videos with AI-powered transcript analysis.

## 🚀 Features

- **Smart Search**: Natural language question processing
- **Real-time Results**: Instant search with debounced input
- **Accessible Design**: WCAG compliant with keyboard navigation
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Dark Mode Support**: Automatic theme switching
- **Error Handling**: Comprehensive error states and retry mechanisms
- **Loading States**: Smooth loading animations and feedback

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **CSS Variables** - Modern styling with dark mode support
- **Lodash** - Utility functions (debouncing)
- **Jest + React Testing Library** - Comprehensive testing

## 📦 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp env.example .env.local
   ```
   Edit `.env.local` and set your API URL:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

## 🧪 Testing

Run the test suite:
```bash
npm test
```

Run tests in watch mode:
```bash
npm run test:watch
```

## 🏗️ Build

Create production build:
```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## 🎨 Styling

The app uses CSS variables for theming and supports:
- **Light/Dark Mode**: Automatic switching based on system preference
- **Responsive Design**: Mobile-first approach
- **Accessibility**: High contrast ratios and focus management
- **Smooth Animations**: With reduced motion support

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

### Vite Configuration

- **Port**: 3000 (configurable)
- **Host**: External connections allowed
- **Auto-open**: Browser opens on dev server start
- **Source maps**: Enabled for debugging

## 📁 Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/
│   │   ├── SearchBar.js    # Search input component
│   │   └── ResultCard.js   # Video result display
│   ├── App.js              # Main application component
│   ├── App.css             # Global styles
│   ├── index.js            # Application entry point
│   └── setupTests.js       # Test configuration
├── tests/
│   └── test_frontend.js    # Component tests
├── package.json            # Dependencies and scripts
├── vite.config.js          # Vite configuration
├── jest.config.js          # Jest configuration
├── .babelrc               # Babel configuration
└── env.example            # Environment variables template
```

## 🧪 Testing Strategy

- **Unit Tests**: Component behavior and props
- **Integration Tests**: API interactions and state management
- **Accessibility Tests**: ARIA labels and keyboard navigation
- **Error Handling**: Network failures and edge cases

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Environment Setup
1. Set `VITE_API_URL` to your production API endpoint
2. Ensure CORS is configured on the backend
3. Deploy the `dist` folder to your hosting service

### Recommended Hosting
- **Vercel**: Zero-config deployment
- **Netlify**: Static site hosting
- **GitHub Pages**: Free hosting for public repos

## 🔍 Development Guidelines

### Code Style
- Use functional components with hooks
- Implement proper error boundaries
- Add accessibility attributes
- Write comprehensive tests

### Performance
- Debounce search inputs
- Lazy load components when needed
- Optimize bundle size
- Use React.memo for expensive components

### Accessibility
- Semantic HTML structure
- ARIA labels and descriptions
- Keyboard navigation support
- Screen reader compatibility

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   - Check `VITE_API_URL` in environment variables
   - Ensure backend server is running
   - Verify CORS configuration

2. **Tests Failing**
   - Run `npm install` to ensure all dependencies
   - Check Jest configuration
   - Verify test environment setup

3. **Build Errors**
   - Clear node_modules and reinstall
   - Check for syntax errors
   - Verify all imports are correct

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is part of the Fewfinder application. See the main README for license information. 