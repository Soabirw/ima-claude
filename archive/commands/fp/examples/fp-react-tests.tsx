/**
 * FP React Tests - Reference Implementation
 * 
 * Demonstrates 100% testable React components through:
 * - Pure component testing via dependency injection
 * - Custom hook testing in isolation
 * - Integration testing with HOCs
 * - Performance testing patterns
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderHook, act } from '@testing-library/react';
import { jest } from '@jest/globals';

// Test utilities for mocking
import { 
  UserCardPure, 
  UserList, 
  useUserManagement, 
  useForm,
  Modal,
  Button 
} from './fp-react-components';
import { withAppConfig, withServices } from './fp-react-hocs';

// ===== MOCK DATA AND UTILITIES =====

const mockUser = {
  id: '1',
  name: 'John Doe',
  email: 'john@example.com',
  role: 'admin' as const,
  isActive: true,
  lastLogin: new Date('2023-12-01')
};

const mockUsers = [
  mockUser,
  {
    id: '2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    role: 'user' as const,
    isActive: true,
    lastLogin: new Date('2023-11-30')
  },
  {
    id: '3',
    name: 'Bob Johnson',
    email: 'bob@example.com',
    role: 'guest' as const,
    isActive: false
  }
];

const mockAppConfig = {
  theme: {
    mode: 'light' as const,
    primaryColor: '#3B82F6',
    borderRadius: '0.5rem'
  },
  features: {
    showAdvancedControls: true,
    enableAnimations: true,
    debugMode: false
  },
  api: {
    baseUrl: 'https://api.test.com',
    timeout: 5000
  }
};

const mockServices = {
  analytics: {
    track: jest.fn(),
    identify: jest.fn()
  },
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn()
  },
  api: {
    get: jest.fn(),
    post: jest.fn()
  }
};

// ===== PURE COMPONENT TESTS =====

describe('UserCardPure', () => {
  const defaultProps = {
    user: mockUser,
    isSelected: false,
    variant: 'compact' as const,
    showEmail: true
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    it('renders user name correctly', () => {
      render(<UserCardPure {...defaultProps} />);
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    it('shows email when showEmail is true and variant is detailed', () => {
      render(
        <UserCardPure 
          {...defaultProps} 
          variant="detailed" 
          showEmail={true} 
        />
      );
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });

    it('hides email when showEmail is false', () => {
      render(
        <UserCardPure 
          {...defaultProps} 
          variant="detailed" 
          showEmail={false} 
        />
      );
      expect(screen.queryByText('john@example.com')).not.toBeInTheDocument();
    });

    it('displays active status badge', () => {
      render(<UserCardPure {...defaultProps} />);
      expect(screen.getByText('Active')).toBeInTheDocument();
    });

    it('displays role badge correctly', () => {
      render(<UserCardPure {...defaultProps} />);
      expect(screen.getByText('admin')).toBeInTheDocument();
    });

    it('shows last login date in detailed variant', () => {
      render(
        <UserCardPure 
          {...defaultProps} 
          variant="detailed" 
        />
      );
      expect(screen.getByText(/Last login:/)).toBeInTheDocument();
    });
  });

  describe('Interactions', () => {
    it('calls onSelect when clicked', async () => {
      const mockOnSelect = jest.fn();
      const user = userEvent.setup();
      
      render(
        <UserCardPure 
          {...defaultProps} 
          onSelect={mockOnSelect} 
        />
      );

      await user.click(screen.getByRole('button'));
      expect(mockOnSelect).toHaveBeenCalledWith('1');
      expect(mockOnSelect).toHaveBeenCalledTimes(1);
    });

    it('does not call onSelect when not provided', async () => {
      const user = userEvent.setup();
      
      render(<UserCardPure {...defaultProps} />);

      // Should not throw when clicking without onSelect
      const element = screen.getByText('John Doe');
      await user.click(element);
    });

    it('calls onEdit when edit button is clicked', async () => {
      const mockOnEdit = jest.fn();
      const user = userEvent.setup();
      
      render(
        <UserCardPure 
          {...defaultProps} 
          onEdit={mockOnEdit} 
        />
      );

      await user.click(screen.getByTitle('Edit user'));
      expect(mockOnEdit).toHaveBeenCalledWith('1');
    });

    it('prevents event propagation on edit button click', async () => {
      const mockOnSelect = jest.fn();
      const mockOnEdit = jest.fn();
      const user = userEvent.setup();
      
      render(
        <UserCardPure 
          {...defaultProps} 
          onSelect={mockOnSelect}
          onEdit={mockOnEdit} 
        />
      );

      await user.click(screen.getByTitle('Edit user'));
      
      expect(mockOnEdit).toHaveBeenCalledWith('1');
      expect(mockOnSelect).not.toHaveBeenCalled();
    });
  });

  describe('Styling', () => {
    it('applies selected styling when isSelected is true', () => {
      const { container } = render(
        <UserCardPure {...defaultProps} isSelected={true} />
      );
      
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('ring-2', 'ring-blue-500');
    });

    it('applies inactive styling when user is inactive', () => {
      const inactiveUser = { ...mockUser, isActive: false };
      const { container } = render(
        <UserCardPure {...defaultProps} user={inactiveUser} />
      );
      
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('opacity-60');
    });

    it('applies custom className', () => {
      const { container } = render(
        <UserCardPure {...defaultProps} className="custom-class" />
      );
      
      const card = container.firstChild as HTMLElement;
      expect(card).toHaveClass('custom-class');
    });
  });

  describe('Accessibility', () => {
    it('has proper role when interactive', () => {
      render(
        <UserCardPure 
          {...defaultProps} 
          onSelect={jest.fn()} 
        />
      );
      
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('has proper tabIndex when interactive', () => {
      render(
        <UserCardPure 
          {...defaultProps} 
          onSelect={jest.fn()} 
        />
      );
      
      const card = screen.getByRole('button');
      expect(card).toHaveAttribute('tabIndex', '0');
    });

    it('does not have role when not interactive', () => {
      render(<UserCardPure {...defaultProps} />);
      
      expect(screen.queryByRole('button')).not.toBeInTheDocument();
    });
  });

  describe('Edge Cases', () => {
    it('handles undefined lastLogin gracefully', () => {
      const userWithoutLogin = { ...mockUser, lastLogin: undefined };
      
      expect(() => {
        render(
          <UserCardPure 
            {...defaultProps} 
            user={userWithoutLogin}
            variant="detailed" 
          />
        );
      }).not.toThrow();
    });

    it('handles long user names with truncation', () => {
      const userWithLongName = { 
        ...mockUser, 
        name: 'This is a very long user name that should be truncated'
      };
      
      render(<UserCardPure {...defaultProps} user={userWithLongName} />);
      
      const nameElement = screen.getByText(userWithLongName.name);
      expect(nameElement).toHaveClass('truncate');
    });
  });
});

// ===== CUSTOM HOOK TESTS =====

describe('useUserManagement', () => {
  it('filters users correctly', () => {
    const { result } = renderHook(() => 
      useUserManagement(mockUsers, { role: 'admin' })
    );

    expect(result.current.filteredUsers).toHaveLength(1);
    expect(result.current.filteredUsers[0].role).toBe('admin');
  });

  it('calculates statistics correctly', () => {
    const { result } = renderHook(() => useUserManagement(mockUsers));

    expect(result.current.statistics).toEqual({
      total: 3,
      active: 2,
      inactive: 1,
      byRole: { admin: 1, user: 1, guest: 1 }
    });
  });

  it('updates filters correctly', () => {
    const { result } = renderHook(() => useUserManagement(mockUsers));

    act(() => {
      result.current.handlers.updateFilters({ isActive: true });
    });

    expect(result.current.filteredUsers).toHaveLength(2);
    expect(result.current.filteredUsers.every(u => u.isActive)).toBe(true);
  });

  it('manages selected users correctly', () => {
    const { result } = renderHook(() => useUserManagement(mockUsers));

    // Select user
    act(() => {
      result.current.handlers.selectUser('1');
    });

    expect(result.current.selectedUsers.has('1')).toBe(true);
    expect(result.current.selectedUsers.size).toBe(1);

    // Toggle (deselect) user
    act(() => {
      result.current.handlers.toggleUser('1');
    });

    expect(result.current.selectedUsers.has('1')).toBe(false);
    expect(result.current.selectedUsers.size).toBe(0);
  });

  it('selects all users correctly', () => {
    const { result } = renderHook(() => useUserManagement(mockUsers));

    act(() => {
      result.current.handlers.selectAll();
    });

    expect(result.current.selectedUsers.size).toBe(3);
    mockUsers.forEach(user => {
      expect(result.current.selectedUsers.has(user.id)).toBe(true);
    });
  });

  it('returns action objects from handlers', () => {
    const { result } = renderHook(() => useUserManagement(mockUsers));

    let action: any;
    
    act(() => {
      action = result.current.handlers.selectUser('1');
    });

    expect(action).toEqual({
      type: 'USER_SELECTED',
      payload: '1'
    });
  });
});

describe('useForm', () => {
  const initialValues = {
    name: '',
    email: '',
    age: 0
  };

  const validationRules = {
    name: { required: true },
    email: { 
      required: true,
      validator: (value: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value) ? null : 'Invalid email format';
      }
    },
    age: {
      validator: (value: number) => {
        return value >= 18 ? null : 'Must be at least 18 years old';
      }
    }
  };

  it('initializes with correct values', () => {
    const { result } = renderHook(() => 
      useForm(initialValues, validationRules)
    );

    expect(result.current.values).toEqual(initialValues);
    expect(result.current.isValid).toBe(true);
    expect(result.current.isDirty).toBe(false);
  });

  it('updates values correctly', () => {
    const { result } = renderHook(() => 
      useForm(initialValues, validationRules)
    );

    act(() => {
      result.current.handlers.setValue('name', 'John Doe');
    });

    expect(result.current.values.name).toBe('John Doe');
    expect(result.current.isDirty).toBe(true);
  });

  it('validates required fields', () => {
    const { result } = renderHook(() => 
      useForm(initialValues, validationRules)
    );

    act(() => {
      result.current.handlers.setTouched('name');
    });

    expect(result.current.errors.name).toBe('name is required');
    expect(result.current.isValid).toBe(false);
  });

  it('validates custom validators', () => {
    const { result } = renderHook(() => 
      useForm(initialValues, validationRules)
    );

    act(() => {
      result.current.handlers.setValue('email', 'invalid-email');
      result.current.handlers.setTouched('email');
    });

    expect(result.current.errors.email).toBe('Invalid email format');
  });

  it('validates all fields correctly', () => {
    const { result } = renderHook(() => 
      useForm({ ...initialValues, age: 16 }, validationRules)
    );

    let isValid: boolean;
    act(() => {
      isValid = result.current.validateAll();
    });

    expect(isValid).toBe(false);
    expect(result.current.errors.name).toBe('name is required');
    expect(result.current.errors.email).toBe('email is required');
    expect(result.current.errors.age).toBe('Must be at least 18 years old');
  });

  it('resets form correctly', () => {
    const { result } = renderHook(() => 
      useForm(initialValues, validationRules)
    );

    // Make changes
    act(() => {
      result.current.handlers.setValue('name', 'John');
      result.current.handlers.setTouched('name');
    });

    // Reset
    act(() => {
      result.current.handlers.resetForm();
    });

    expect(result.current.values).toEqual(initialValues);
    expect(result.current.errors).toEqual({});
    expect(result.current.touched).toEqual({});
    expect(result.current.isDirty).toBe(false);
  });
});

// ===== INTEGRATION TESTS WITH HOCS =====

describe('HOC Integration Tests', () => {
  // Create a test component with injected dependencies
  const TestComponent = ({ 
    appConfig, 
    services, 
    title 
  }: { 
    appConfig: any; 
    services: any; 
    title: string; 
  }) => {
    const handleClick = () => {
      services.analytics.track('test_clicked', { title });
    };

    return (
      <div data-testid="test-component">
        <h1>{title}</h1>
        <p>Theme: {appConfig.theme.mode}</p>
        <p>Features: {JSON.stringify(appConfig.features)}</p>
        <button onClick={handleClick}>Track Event</button>
      </div>
    );
  };

  it('injects app config correctly', () => {
    // Mock the hook that provides config
    const mockUseAppConfiguration = jest.fn().mockReturnValue(mockAppConfig);
    
    // Component with app config injection
    const EnhancedComponent = withAppConfig(TestComponent);
    
    render(
      <EnhancedComponent 
        title="Test Title" 
      />
    );

    expect(screen.getByText('Theme: light')).toBeInTheDocument();
    expect(screen.getByText(/showAdvancedControls.*true/)).toBeInTheDocument();
  });

  it('injects services correctly and tracks analytics', async () => {
    // Mock the services hook
    const mockUseServices = jest.fn().mockReturnValue(mockServices);
    
    // Component with services injection
    const EnhancedComponent = withServices(TestComponent);
    
    render(
      <EnhancedComponent 
        title="Test Title"
        appConfig={mockAppConfig}
      />
    );

    const button = screen.getByText('Track Event');
    await userEvent.setup().click(button);

    expect(mockServices.analytics.track).toHaveBeenCalledWith('test_clicked', {
      title: 'Test Title'
    });
  });
});

// ===== COMPOUND COMPONENT TESTS =====

describe('Modal Compound Component', () => {
  it('renders when open', () => {
    render(
      <Modal isOpen={true} onClose={jest.fn()}>
        <Modal.Content>
          <Modal.Header>Test Header</Modal.Header>
          <Modal.Body>Test Body</Modal.Body>
        </Modal.Content>
      </Modal>
    );

    expect(screen.getByText('Test Header')).toBeInTheDocument();
    expect(screen.getByText('Test Body')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={jest.fn()}>
        <Modal.Content>
          <Modal.Body>Test Body</Modal.Body>
        </Modal.Content>
      </Modal>
    );

    expect(screen.queryByText('Test Body')).not.toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', async () => {
    const mockOnClose = jest.fn();
    const user = userEvent.setup();

    render(
      <Modal isOpen={true} onClose={mockOnClose}>
        <Modal.Content>
          <Modal.Header>Test Header</Modal.Header>
        </Modal.Content>
      </Modal>
    );

    await user.click(screen.getByTitle('Close'));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when escape key is pressed', async () => {
    const mockOnClose = jest.fn();
    const user = userEvent.setup();

    render(
      <Modal isOpen={true} onClose={mockOnClose}>
        <Modal.Content>
          <Modal.Body>Test Body</Modal.Body>
        </Modal.Content>
      </Modal>
    );

    await user.keyboard('{Escape}');
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when overlay is clicked', async () => {
    const mockOnClose = jest.fn();
    const user = userEvent.setup();

    render(
      <Modal isOpen={true} onClose={mockOnClose}>
        <Modal.Content>
          <Modal.Body>Test Body</Modal.Body>
        </Modal.Content>
      </Modal>
    );

    // Click on overlay (not on modal content)
    const overlay = screen.getByRole('dialog').parentElement;
    await user.click(overlay!);
    
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('does not close on overlay click when disabled', async () => {
    const mockOnClose = jest.fn();
    const user = userEvent.setup();

    render(
      <Modal isOpen={true} onClose={mockOnClose} closeOnOverlayClick={false}>
        <Modal.Content>
          <Modal.Body>Test Body</Modal.Body>
        </Modal.Content>
      </Modal>
    );

    const overlay = screen.getByRole('dialog').parentElement;
    await user.click(overlay!);
    
    expect(mockOnClose).not.toHaveBeenCalled();
  });
});

// ===== PERFORMANCE TESTS =====

describe('Performance Tests', () => {
  it('UserCardPure should not re-render when props are the same', () => {
    const renderSpy = jest.fn();
    
    const TestUserCard = (props: any) => {
      renderSpy();
      return <UserCardPure {...props} />;
    };

    const { rerender } = render(
      <TestUserCard {...{ user: mockUser, isSelected: false, variant: 'compact', showEmail: true }} />
    );

    expect(renderSpy).toHaveBeenCalledTimes(1);

    // Re-render with same props
    rerender(
      <TestUserCard {...{ user: mockUser, isSelected: false, variant: 'compact', showEmail: true }} />
    );

    // Should not re-render due to memoization
    expect(renderSpy).toHaveBeenCalledTimes(1);
  });

  it('Button should handle rapid clicks correctly', async () => {
    const mockOnClick = jest.fn();
    const user = userEvent.setup();

    render(
      <Button onClick={mockOnClick}>
        Click me
      </Button>
    );

    const button = screen.getByText('Click me');

    // Rapid clicks
    await user.click(button);
    await user.click(button);
    await user.click(button);

    expect(mockOnClick).toHaveBeenCalledTimes(3);
  });

  it('should handle loading state correctly', () => {
    const { rerender } = render(
      <Button isLoading={false} onClick={jest.fn()}>
        Submit
      </Button>
    );

    expect(screen.getByText('Submit')).toBeEnabled();

    rerender(
      <Button isLoading={true} onClick={jest.fn()}>
        Submit
      </Button>
    );

    expect(screen.getByText('Submit')).toBeDisabled();
    expect(screen.getByRole('button')).toHaveClass('opacity-75');
  });
});

// ===== TEST UTILITIES =====

/**
 * Test utility for creating mock services
 */
export const createMockServices = (overrides = {}) => ({
  analytics: {
    track: jest.fn(),
    identify: jest.fn(),
    ...overrides.analytics
  },
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    ...overrides.logger
  },
  api: {
    get: jest.fn().mockResolvedValue({}),
    post: jest.fn().mockResolvedValue({}),
    ...overrides.api
  }
});

/**
 * Test utility for creating mock app config
 */
export const createMockAppConfig = (overrides = {}) => ({
  theme: {
    mode: 'light' as const,
    primaryColor: '#3B82F6',
    borderRadius: '0.5rem',
    ...overrides.theme
  },
  features: {
    showAdvancedControls: true,
    enableAnimations: true,
    debugMode: false,
    ...overrides.features
  },
  api: {
    baseUrl: 'https://api.test.com',
    timeout: 5000,
    ...overrides.api
  }
});

/**
 * Test utility for rendering components with providers
 */
export const renderWithProviders = (
  component: React.ReactElement,
  options: {
    appConfig?: any;
    services?: any;
  } = {}
) => {
  const { appConfig, services } = options;
  
  let WrappedComponent = component;
  
  if (services) {
    // Mock services provider
    const ServicesProvider = ({ children }: { children: React.ReactNode }) => {
      // Mock implementation
      return <>{children}</>;
    };
    WrappedComponent = <ServicesProvider>{WrappedComponent}</ServicesProvider>;
  }
  
  if (appConfig) {
    // Mock app config provider
    const AppConfigProvider = ({ children }: { children: React.ReactNode }) => {
      // Mock implementation
      return <>{children}</>;
    };
    WrappedComponent = <AppConfigProvider>{WrappedComponent}</AppConfigProvider>;
  }
  
  return render(WrappedComponent);
};

export default {
  mockUser,
  mockUsers,
  mockAppConfig,
  mockServices,
  createMockServices,
  createMockAppConfig,
  renderWithProviders
};