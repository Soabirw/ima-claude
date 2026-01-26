/**
 * FP React HOCs - Reference Implementation
 * 
 * Strategic Higher-Order Components for:
 * - Dependency injection
 * - Cross-cutting concerns
 * - Pure component enablement
 * - Testability enhancement
 */

import React, { 
  ComponentType, 
  ErrorInfo, 
  ReactNode, 
  createContext, 
  useContext,
  useState,
  useEffect,
  useRef
} from 'react';

// ===== DEPENDENCY INJECTION HOCS =====

/**
 * Configuration Injection HOC
 * 
 * Injects application configuration for testable components.
 * Enables pure components to receive config without prop drilling.
 */

interface AppConfig {
  theme: {
    mode: 'light' | 'dark';
    primaryColor: string;
    borderRadius: string;
  };
  features: {
    showAdvancedControls: boolean;
    enableAnimations: boolean;
    debugMode: boolean;
  };
  api: {
    baseUrl: string;
    timeout: number;
  };
}

// Mock hook - replace with your actual configuration hook
const useAppConfiguration = (): AppConfig => ({
  theme: {
    mode: 'light',
    primaryColor: '#3B82F6',
    borderRadius: '0.5rem'
  },
  features: {
    showAdvancedControls: false,
    enableAnimations: true,
    debugMode: process.env.NODE_ENV === 'development'
  },
  api: {
    baseUrl: 'https://api.example.com',
    timeout: 5000
  }
});

export const withAppConfig = <P extends {}>(
  Component: ComponentType<P & { appConfig: AppConfig }>
) => {
  const WithAppConfig = (props: P) => {
    const appConfig = useAppConfiguration();
    
    return <Component {...props} appConfig={appConfig} />;
  };
  
  WithAppConfig.displayName = `withAppConfig(${Component.displayName || Component.name})`;
  return WithAppConfig;
};

/**
 * Service Injection HOC
 * 
 * Injects services like analytics, logging, API clients.
 * Enables testing by injecting mock services.
 */

interface Services {
  analytics: {
    track: (event: string, properties?: Record<string, any>) => void;
    identify: (userId: string, traits?: Record<string, any>) => void;
  };
  logger: {
    info: (message: string, meta?: any) => void;
    warn: (message: string, meta?: any) => void;
    error: (message: string, meta?: any) => void;
  };
  api: {
    get: <T>(url: string) => Promise<T>;
    post: <T>(url: string, data: any) => Promise<T>;
  };
}

// Mock services - replace with your actual services
const useServices = (): Services => ({
  analytics: {
    track: (event, properties) => console.log('📊 Track:', event, properties),
    identify: (userId, traits) => console.log('👤 Identify:', userId, traits)
  },
  logger: {
    info: (message, meta) => console.info('ℹ️', message, meta),
    warn: (message, meta) => console.warn('⚠️', message, meta),
    error: (message, meta) => console.error('❌', message, meta)
  },
  api: {
    get: async (url) => {
      const response = await fetch(url);
      return response.json();
    },
    post: async (url, data) => {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return response.json();
    }
  }
});

export const withServices = <P extends {}>(
  Component: ComponentType<P & { services: Services }>
) => {
  const WithServices = (props: P) => {
    const services = useServices();
    
    return <Component {...props} services={services} />;
  };
  
  WithServices.displayName = `withServices(${Component.displayName || Component.name})`;
  return WithServices;
};

// ===== CROSS-CUTTING CONCERNS HOCS =====

/**
 * Error Boundary HOC
 * 
 * Catches and handles component errors gracefully.
 * Provides fallback UI and error reporting.
 */

interface ErrorFallbackProps {
  error: Error;
  resetError: () => void;
  componentName?: string;
}

const DefaultErrorFallback = ({ error, resetError, componentName }: ErrorFallbackProps) => (
  <div className="error-boundary p-6 bg-red-50 border border-red-200 rounded-lg">
    <h3 className="text-lg font-semibold text-red-800 mb-2">
      Something went wrong{componentName && ` in ${componentName}`}
    </h3>
    <details className="mb-4">
      <summary className="cursor-pointer text-red-600 hover:text-red-700">
        Error details
      </summary>
      <pre className="mt-2 p-3 bg-red-100 rounded text-sm text-red-700 overflow-auto">
        {error.message}
        {process.env.NODE_ENV === 'development' && error.stack && (
          <div className="mt-2 text-xs">{error.stack}</div>
        )}
      </pre>
    </details>
    <button 
      onClick={resetError}
      className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
    >
      Try again
    </button>
  </div>
);

export const withErrorBoundary = <P extends {}>(
  Component: ComponentType<P>,
  customFallback?: ComponentType<ErrorFallbackProps>
) => {
  const FallbackComponent = customFallback || DefaultErrorFallback;
  
  return class WithErrorBoundary extends React.Component<
    P, 
    { hasError: boolean; error: Error | null }
  > {
    constructor(props: P) {
      super(props);
      this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error: Error) {
      return { hasError: true, error };
    }
    
    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
      // Log error to monitoring service
      console.error('Component error boundary caught:', {
        error: error.message,
        componentStack: errorInfo.componentStack,
        componentName: Component.displayName || Component.name
      });
      
      // Report to error monitoring service (e.g., Sentry)
      if (typeof window !== 'undefined' && (window as any).Sentry) {
        (window as any).Sentry.captureException(error, {
          contexts: {
            react: {
              componentStack: errorInfo.componentStack
            }
          }
        });
      }
    }
    
    resetError = () => {
      this.setState({ hasError: false, error: null });
    };
    
    render() {
      if (this.state.hasError) {
        return (
          <FallbackComponent 
            error={this.state.error!} 
            resetError={this.resetError}
            componentName={Component.displayName || Component.name}
          />
        );
      }
      
      return <Component {...this.props} />;
    }
    
    static displayName = `withErrorBoundary(${Component.displayName || Component.name})`;
  };
};

/**
 * Loading State HOC
 * 
 * Handles loading states consistently across components.
 */

interface LoadingProps {
  isLoading?: boolean;
  loadingComponent?: ReactNode;
  loadingText?: string;
}

const DefaultLoadingComponent = ({ text = 'Loading...' }: { text?: string }) => (
  <div className="loading-spinner flex items-center justify-center p-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mr-3"></div>
    <span className="text-gray-600">{text}</span>
  </div>
);

export const withLoadingState = <P extends {}>(
  Component: ComponentType<P>
) => {
  const WithLoadingState = (props: P & LoadingProps) => {
    const { 
      isLoading, 
      loadingComponent, 
      loadingText, 
      ...componentProps 
    } = props;
    
    if (isLoading) {
      return loadingComponent || <DefaultLoadingComponent text={loadingText} />;
    }
    
    return <Component {...(componentProps as P)} />;
  };
  
  WithLoadingState.displayName = `withLoadingState(${Component.displayName || Component.name})`;
  return WithLoadingState;
};

/**
 * Analytics HOC
 * 
 * Automatically tracks component interactions and lifecycle events.
 */

interface AnalyticsOptions {
  trackMount?: boolean;
  trackUnmount?: boolean;
  trackProps?: boolean;
  eventPrefix?: string;
}

export const withAnalytics = <P extends {}>(
  Component: ComponentType<P>,
  options: AnalyticsOptions = {}
) => {
  const {
    trackMount = true,
    trackUnmount = false,
    trackProps = false,
    eventPrefix = ''
  } = options;
  
  const WithAnalytics = (props: P) => {
    const services = useServices();
    const componentName = Component.displayName || Component.name;
    const mountedRef = useRef(false);
    
    useEffect(() => {
      if (trackMount && !mountedRef.current) {
        services.analytics.track(
          `${eventPrefix}${componentName}_mounted`,
          trackProps ? { props } : undefined
        );
        mountedRef.current = true;
      }
      
      return () => {
        if (trackUnmount) {
          services.analytics.track(`${eventPrefix}${componentName}_unmounted`);
        }
      };
    }, [services.analytics, componentName, props]);
    
    return <Component {...props} />;
  };
  
  WithAnalytics.displayName = `withAnalytics(${Component.displayName || Component.name})`;
  return WithAnalytics;
};

/**
 * Performance Monitoring HOC
 * 
 * Monitors component render performance and logs slow renders.
 */

interface PerformanceOptions {
  slowThreshold?: number; // milliseconds
  enableInProduction?: boolean;
}

export const withPerformanceMonitoring = <P extends {}>(
  Component: ComponentType<P>,
  options: PerformanceOptions = {}
) => {
  const { slowThreshold = 16, enableInProduction = false } = options;
  
  // Skip in production unless explicitly enabled
  if (process.env.NODE_ENV === 'production' && !enableInProduction) {
    return Component;
  }
  
  const WithPerformanceMonitoring = (props: P) => {
    const componentName = Component.displayName || Component.name;
    const renderStartRef = useRef(0);
    const renderCountRef = useRef(0);
    
    // Start timing
    renderStartRef.current = performance.now();
    renderCountRef.current += 1;
    
    useEffect(() => {
      // End timing after render
      const renderTime = performance.now() - renderStartRef.current;
      
      if (renderTime > slowThreshold) {
        console.warn(
          `🐌 Slow render detected: ${componentName} took ${renderTime.toFixed(2)}ms ` +
          `(render #${renderCountRef.current})`
        );
      }
    });
    
    return <Component {...props} />;
  };
  
  WithPerformanceMonitoring.displayName = `withPerformanceMonitoring(${Component.displayName || Component.name})`;
  return WithPerformanceMonitoring;
};

// ===== UTILITY HOCS =====

/**
 * Props Validation HOC
 * 
 * Runtime prop validation with detailed error messages.
 */

type PropValidator<T> = (value: T, propName: string) => string | null;

export const withPropsValidation = <P extends {}>(
  Component: ComponentType<P>,
  validators: Partial<{ [K in keyof P]: PropValidator<P[K]> }>
) => {
  const WithPropsValidation = (props: P) => {
    // Only validate in development
    if (process.env.NODE_ENV === 'development') {
      Object.entries(validators).forEach(([propName, validator]) => {
        const propValue = props[propName as keyof P];
        const error = (validator as PropValidator<any>)?.(propValue, propName);
        
        if (error) {
          console.error(
            `❌ Prop validation failed for '${propName}' in ${Component.displayName || Component.name}: ${error}`,
            { receivedValue: propValue }
          );
        }
      });
    }
    
    return <Component {...props} />;
  };
  
  WithPropsValidation.displayName = `withPropsValidation(${Component.displayName || Component.name})`;
  return WithPropsValidation;
};

/**
 * Conditional Rendering HOC
 * 
 * Conditionally render component based on predicate function.
 */

export const withConditionalRender = <P extends {}>(
  Component: ComponentType<P>,
  predicate: (props: P) => boolean,
  fallback?: ComponentType<P> | ReactNode
) => {
  const WithConditionalRender = (props: P) => {
    if (!predicate(props)) {
      if (React.isValidElement(fallback)) {
        return fallback;
      }
      if (typeof fallback === 'function') {
        const FallbackComponent = fallback as ComponentType<P>;
        return <FallbackComponent {...props} />;
      }
      return null;
    }
    
    return <Component {...props} />;
  };
  
  WithConditionalRender.displayName = `withConditionalRender(${Component.displayName || Component.name})`;
  return WithConditionalRender;
};

// ===== HOC COMPOSITION UTILITIES =====

/**
 * Compose multiple HOCs into a single HOC
 * 
 * Prevents deep nesting and improves readability.
 */
export const compose = <T extends any[]>(...hocs: T): T[0] =>
  hocs.reduce((acc, hoc) => hoc(acc));

/**
 * Create HOC with multiple concerns
 * 
 * Factory for creating components with multiple cross-cutting concerns.
 */
export const createEnhancedComponent = <P extends {}>(
  Component: ComponentType<P>,
  enhancements: {
    errorBoundary?: boolean | ComponentType<ErrorFallbackProps>;
    loading?: boolean;
    analytics?: boolean | AnalyticsOptions;
    performance?: boolean | PerformanceOptions;
    config?: boolean;
    services?: boolean;
  } = {}
) => {
  let EnhancedComponent = Component;
  
  // Apply enhancements in logical order
  if (enhancements.config) {
    EnhancedComponent = withAppConfig(EnhancedComponent);
  }
  
  if (enhancements.services) {
    EnhancedComponent = withServices(EnhancedComponent);
  }
  
  if (enhancements.performance) {
    const options = typeof enhancements.performance === 'object' 
      ? enhancements.performance 
      : {};
    EnhancedComponent = withPerformanceMonitoring(EnhancedComponent, options);
  }
  
  if (enhancements.analytics) {
    const options = typeof enhancements.analytics === 'object' 
      ? enhancements.analytics 
      : {};
    EnhancedComponent = withAnalytics(EnhancedComponent, options);
  }
  
  if (enhancements.loading) {
    EnhancedComponent = withLoadingState(EnhancedComponent);
  }
  
  if (enhancements.errorBoundary) {
    const fallback = typeof enhancements.errorBoundary === 'function'
      ? enhancements.errorBoundary
      : undefined;
    EnhancedComponent = withErrorBoundary(EnhancedComponent, fallback);
  }
  
  return EnhancedComponent;
};

// ===== EXAMPLE USAGE =====

// Example of a pure component that receives injected dependencies
interface ExampleComponentProps {
  title: string;
  data: any[];
  appConfig: AppConfig; // Injected by withAppConfig
  services: Services;    // Injected by withServices
}

const ExamplePureComponent = ({ title, data, appConfig, services }: ExampleComponentProps) => {
  const handleClick = () => {
    services.analytics.track('example_clicked', { title });
    services.logger.info('Example component clicked', { title });
  };
  
  return (
    <div 
      className="p-4 rounded-lg"
      style={{ 
        backgroundColor: appConfig.theme.mode === 'dark' ? '#1f2937' : '#f9fafb',
        borderRadius: appConfig.theme.borderRadius
      }}
    >
      <h2 className="text-xl font-bold mb-4">{title}</h2>
      <button 
        onClick={handleClick}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        disabled={!appConfig.features.showAdvancedControls}
      >
        Click me
      </button>
      <div className="mt-4">
        {data.map((item, index) => (
          <div key={index} className="p-2 border-b">
            {JSON.stringify(item)}
          </div>
        ))}
      </div>
    </div>
  );
};

// Enhanced component with all cross-cutting concerns
export const EnhancedExampleComponent = createEnhancedComponent(
  ExamplePureComponent,
  {
    errorBoundary: true,
    loading: true,
    analytics: { trackMount: true, trackProps: true },
    performance: { slowThreshold: 20 },
    config: true,
    services: true
  }
);

export default {
  withAppConfig,
  withServices,
  withErrorBoundary,
  withLoadingState,
  withAnalytics,
  withPerformanceMonitoring,
  withPropsValidation,
  withConditionalRender,
  compose,
  createEnhancedComponent
};