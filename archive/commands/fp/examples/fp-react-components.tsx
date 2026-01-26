/**
 * FP React Components - Reference Implementation
 * 
 * Examples of:
 * - Pure components with custom hooks
 * - Compound component patterns
 * - Performance-optimized components
 * - Highly testable architecture
 */

import React, { 
  memo, 
  useMemo, 
  useCallback, 
  createContext, 
  useContext,
  ReactNode,
  useState,
  useRef,
  useEffect
} from 'react';
import { createClassMap, createButtonClasses, createSetOperations } from './fp-react-utils';
import { withAppConfig, withServices } from './fp-react-hocs';

// ===== CUSTOM HOOKS FOR BUSINESS LOGIC =====

/**
 * User Management Hook
 * 
 * Separates all user-related business logic from presentation.
 */
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  isActive: boolean;
  lastLogin?: Date;
}

interface UserFilters {
  role?: User['role'];
  isActive?: boolean;
  searchTerm?: string;
}

const useUserManagement = (users: User[], initialFilters: UserFilters = {}) => {
  const [filters, setFilters] = useState(initialFilters);
  const [selectedUsers, setSelectedUsers] = useState<Set<string>>(new Set());
  
  const setOperations = useMemo(() => createSetOperations<string>(), []);
  
  // Pure function for filtering users
  const filteredUsers = useMemo(() => {
    return users.filter(user => {
      if (filters.role && user.role !== filters.role) return false;
      if (filters.isActive !== undefined && user.isActive !== filters.isActive) return false;
      if (filters.searchTerm) {
        const search = filters.searchTerm.toLowerCase();
        return user.name.toLowerCase().includes(search) ||
               user.email.toLowerCase().includes(search);
      }
      return true;
    });
  }, [users, filters]);
  
  // Pure function for user statistics
  const statistics = useMemo(() => {
    const total = filteredUsers.length;
    const active = filteredUsers.filter(u => u.isActive).length;
    const byRole = filteredUsers.reduce((acc, user) => {
      acc[user.role] = (acc[user.role] || 0) + 1;
      return acc;
    }, {} as Record<User['role'], number>);
    
    return { total, active, inactive: total - active, byRole };
  }, [filteredUsers]);
  
  // Event handlers that return action objects
  const handlers = useMemo(() => ({
    updateFilters: (newFilters: Partial<UserFilters>) => {
      setFilters(prev => ({ ...prev, ...newFilters }));
      return { type: 'FILTERS_UPDATED', payload: newFilters };
    },
    
    selectUser: (userId: string) => {
      setSelectedUsers(prev => setOperations.add(prev, userId));
      return { type: 'USER_SELECTED', payload: userId };
    },
    
    deselectUser: (userId: string) => {
      setSelectedUsers(prev => setOperations.remove(prev, userId));
      return { type: 'USER_DESELECTED', payload: userId };
    },
    
    toggleUser: (userId: string) => {
      setSelectedUsers(prev => setOperations.toggle(prev, userId));
      return { type: 'USER_TOGGLED', payload: userId };
    },
    
    selectAll: () => {
      const allIds = filteredUsers.map(u => u.id);
      setSelectedUsers(new Set(allIds));
      return { type: 'ALL_USERS_SELECTED', payload: allIds };
    },
    
    deselectAll: () => {
      setSelectedUsers(new Set());
      return { type: 'ALL_USERS_DESELECTED' };
    }
  }), [filteredUsers, setOperations]);
  
  return {
    filteredUsers,
    statistics,
    filters,
    selectedUsers,
    handlers
  };
};

/**
 * Form Hook with Validation
 * 
 * Generic form handling with pure validation functions.
 */
interface ValidationRule<T> {
  required?: boolean;
  validator?: (value: T) => string | null;
}

type ValidationRules<T> = {
  [K in keyof T]?: ValidationRule<T[K]>;
};

const useForm = <T extends Record<string, any>>(
  initialValues: T,
  validationRules: ValidationRules<T> = {}
) => {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  
  // Pure validation function
  const validateField = useCallback((name: keyof T, value: T[keyof T]): string | null => {
    const rules = validationRules[name];
    if (!rules) return null;
    
    // Required validation
    if (rules.required && (!value || value === '')) {
      return `${String(name)} is required`;
    }
    
    // Custom validation
    if (rules.validator && value) {
      return rules.validator(value);
    }
    
    return null;
  }, [validationRules]);
  
  // Validate all fields
  const validateAll = useCallback((): boolean => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let isValid = true;
    
    Object.keys(values).forEach(key => {
      const error = validateField(key as keyof T, values[key as keyof T]);
      if (error) {
        newErrors[key as keyof T] = error;
        isValid = false;
      }
    });
    
    setErrors(newErrors);
    return isValid;
  }, [values, validateField]);
  
  const handlers = useMemo(() => ({
    setValue: <K extends keyof T>(name: K, value: T[K]) => {
      setValues(prev => ({ ...prev, [name]: value }));
      
      // Validate field if it has been touched
      if (touched[name]) {
        const error = validateField(name, value);
        setErrors(prev => ({ ...prev, [name]: error || undefined }));
      }
      
      return { type: 'FIELD_CHANGED', payload: { name, value } };
    },
    
    setTouched: (name: keyof T) => {
      setTouched(prev => ({ ...prev, [name]: true }));
      
      // Validate field when touched
      const error = validateField(name, values[name]);
      setErrors(prev => ({ ...prev, [name]: error || undefined }));
      
      return { type: 'FIELD_TOUCHED', payload: name };
    },
    
    resetForm: () => {
      setValues(initialValues);
      setErrors({});
      setTouched({});
      return { type: 'FORM_RESET' };
    }
  }), [touched, validateField, values, initialValues]);
  
  const isValid = Object.keys(errors).length === 0;
  const isDirty = JSON.stringify(values) !== JSON.stringify(initialValues);
  
  return {
    values,
    errors,
    touched,
    isValid,
    isDirty,
    handlers,
    validateAll
  };
};

// ===== PURE COMPONENTS =====

/**
 * User Card - Pure Component
 * 
 * Zero business logic, fully testable through props.
 */
interface UserCardProps {
  user: User;
  isSelected: boolean;
  variant: 'compact' | 'detailed';
  showEmail: boolean;
  onSelect?: (userId: string) => void;
  onEdit?: (userId: string) => void;
  className?: string;
}

// Pre-compiled classes for performance
const userCardClasses = createClassMap(
  'user-card relative bg-white rounded-lg shadow-sm border transition-all duration-200',
  {
    compact: 'p-3',
    detailed: 'p-4'
  },
  {
    selected: 'ring-2 ring-blue-500 border-blue-200',
    interactive: 'hover:shadow-md cursor-pointer',
    inactive: 'opacity-60'
  }
);

const UserCardPure = memo<UserCardProps>(({
  user,
  isSelected,
  variant,
  showEmail,
  onSelect,
  onEdit,
  className
}) => {
  const handleClick = useCallback(() => {
    onSelect?.(user.id);
  }, [onSelect, user.id]);
  
  const handleEdit = useCallback((e: React.MouseEvent) => {
    e.stopPropagation();
    onEdit?.(user.id);
  }, [onEdit, user.id]);
  
  const cardClass = userCardClasses(variant, [
    isSelected && 'selected',
    onSelect && 'interactive',
    !user.isActive && 'inactive'
  ].filter(Boolean));
  
  return (
    <div 
      className={`${cardClass} ${className || ''}`}
      onClick={handleClick}
      role={onSelect ? 'button' : undefined}
      tabIndex={onSelect ? 0 : undefined}
    >
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-medium text-gray-900 truncate">
            {user.name}
          </h3>
          {variant === 'detailed' && showEmail && (
            <p className="text-sm text-gray-500 truncate">{user.email}</p>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          <span
            className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
              user.isActive 
                ? 'bg-green-100 text-green-800' 
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {user.isActive ? 'Active' : 'Inactive'}
          </span>
          
          <span
            className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
              user.role === 'admin' 
                ? 'bg-purple-100 text-purple-800'
                : user.role === 'user'
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {user.role}
          </span>
          
          {onEdit && (
            <button
              onClick={handleEdit}
              className="p-1 text-gray-400 hover:text-gray-600 rounded"
              title="Edit user"
            >
              ✏️
            </button>
          )}
        </div>
      </div>
      
      {variant === 'detailed' && user.lastLogin && (
        <div className="mt-2 text-xs text-gray-500">
          Last login: {user.lastLogin.toLocaleDateString()}
        </div>
      )}
    </div>
  );
});

UserCardPure.displayName = 'UserCardPure';

/**
 * User List - Container Component
 * 
 * Combines business logic hook with pure presentation components.
 */
interface UserListProps {
  users: User[];
  initialFilters?: UserFilters;
  variant?: 'compact' | 'detailed';
  showEmail?: boolean;
  onUserAction?: (action: any) => void;
}

const UserList = memo<UserListProps>(({
  users,
  initialFilters,
  variant = 'compact',
  showEmail = true,
  onUserAction
}) => {
  const {
    filteredUsers,
    statistics,
    filters,
    selectedUsers,
    handlers
  } = useUserManagement(users, initialFilters);
  
  const handleUserSelect = useCallback((userId: string) => {
    const action = handlers.toggleUser(userId);
    onUserAction?.(action);
  }, [handlers, onUserAction]);
  
  const handleSelectAll = useCallback(() => {
    const action = selectedUsers.size === filteredUsers.length 
      ? handlers.deselectAll()
      : handlers.selectAll();
    onUserAction?.(action);
  }, [handlers, selectedUsers.size, filteredUsers.length, onUserAction]);
  
  const handleFilterChange = useCallback((newFilters: Partial<UserFilters>) => {
    const action = handlers.updateFilters(newFilters);
    onUserAction?.(action);
  }, [handlers, onUserAction]);
  
  return (
    <div className="user-list space-y-4">
      {/* Filter Controls */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <select
            value={filters.role || ''}
            onChange={(e) => handleFilterChange({ role: e.target.value as User['role'] || undefined })}
            className="border border-gray-300 rounded px-3 py-1 text-sm"
          >
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="user">User</option>
            <option value="guest">Guest</option>
          </select>
          
          <select
            value={filters.isActive === undefined ? '' : filters.isActive.toString()}
            onChange={(e) => {
              const value = e.target.value;
              handleFilterChange({ 
                isActive: value === '' ? undefined : value === 'true' 
              });
            }}
            className="border border-gray-300 rounded px-3 py-1 text-sm"
          >
            <option value="">All Status</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
          
          <input
            type="text"
            placeholder="Search users..."
            value={filters.searchTerm || ''}
            onChange={(e) => handleFilterChange({ searchTerm: e.target.value })}
            className="border border-gray-300 rounded px-3 py-1 text-sm"
          />
        </div>
        
        <div className="text-sm text-gray-500">
          {selectedUsers.size} of {statistics.total} selected
        </div>
      </div>
      
      {/* Statistics */}
      <div className="grid grid-cols-4 gap-4 text-center">
        <div className="bg-gray-50 p-3 rounded">
          <div className="text-2xl font-bold">{statistics.total}</div>
          <div className="text-sm text-gray-600">Total</div>
        </div>
        <div className="bg-green-50 p-3 rounded">
          <div className="text-2xl font-bold text-green-600">{statistics.active}</div>
          <div className="text-sm text-gray-600">Active</div>
        </div>
        <div className="bg-red-50 p-3 rounded">
          <div className="text-2xl font-bold text-red-600">{statistics.inactive}</div>
          <div className="text-sm text-gray-600">Inactive</div>
        </div>
        <div className="bg-blue-50 p-3 rounded">
          <div className="text-2xl font-bold text-blue-600">{statistics.byRole.admin || 0}</div>
          <div className="text-sm text-gray-600">Admins</div>
        </div>
      </div>
      
      {/* Select All Toggle */}
      {filteredUsers.length > 0 && (
        <div className="flex items-center">
          <button
            onClick={handleSelectAll}
            className="flex items-center text-sm text-blue-600 hover:text-blue-700"
          >
            <input
              type="checkbox"
              checked={selectedUsers.size === filteredUsers.length}
              readOnly
              className="mr-2"
            />
            {selectedUsers.size === filteredUsers.length ? 'Deselect All' : 'Select All'}
          </button>
        </div>
      )}
      
      {/* User Cards */}
      <div className="space-y-2">
        {filteredUsers.map(user => (
          <UserCardPure
            key={user.id}
            user={user}
            isSelected={selectedUsers.has(user.id)}
            variant={variant}
            showEmail={showEmail}
            onSelect={handleUserSelect}
          />
        ))}
      </div>
      
      {filteredUsers.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No users match the current filters.
        </div>
      )}
    </div>
  );
});

UserList.displayName = 'UserList';

// ===== COMPOUND COMPONENT PATTERN =====

/**
 * Modal - Compound Component
 * 
 * Flexible, composable modal with context-based communication.
 */
interface ModalContextValue {
  isOpen: boolean;
  close: () => void;
}

const ModalContext = createContext<ModalContextValue | null>(null);

const useModalContext = () => {
  const context = useContext(ModalContext);
  if (!context) {
    throw new Error('Modal compound components must be used within Modal');
  }
  return context;
};

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
}

const Modal = ({
  isOpen,
  onClose,
  children,
  closeOnOverlayClick = true,
  closeOnEscape = true
}: ModalProps) => {
  const overlayRef = useRef<HTMLDivElement>(null);
  
  const contextValue = useMemo(() => ({
    isOpen,
    close: onClose
  }), [isOpen, onClose]);
  
  // Handle escape key
  useEffect(() => {
    if (!closeOnEscape || !isOpen) return;
    
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [closeOnEscape, isOpen, onClose]);
  
  // Handle overlay click
  const handleOverlayClick = useCallback((e: React.MouseEvent) => {
    if (closeOnOverlayClick && e.target === overlayRef.current) {
      onClose();
    }
  }, [closeOnOverlayClick, onClose]);
  
  if (!isOpen) return null;
  
  return (
    <ModalContext.Provider value={contextValue}>
      <div
        ref={overlayRef}
        className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4"
        onClick={handleOverlayClick}
      >
        {children}
      </div>
    </ModalContext.Provider>
  );
};

const ModalContent = ({ children, className }: { children: ReactNode; className?: string }) => {
  return (
    <div className={`bg-white rounded-lg shadow-xl max-w-lg w-full max-h-[90vh] overflow-auto ${className || ''}`}>
      {children}
    </div>
  );
};

const ModalHeader = ({ children, className }: { children: ReactNode; className?: string }) => {
  const { close } = useModalContext();
  
  return (
    <div className={`flex items-center justify-between p-4 border-b ${className || ''}`}>
      <div className="flex-1">{children}</div>
      <button
        onClick={close}
        className="ml-4 text-gray-400 hover:text-gray-600 text-xl"
        title="Close"
      >
        ×
      </button>
    </div>
  );
};

const ModalBody = ({ children, className }: { children: ReactNode; className?: string }) => {
  return (
    <div className={`p-4 ${className || ''}`}>
      {children}
    </div>
  );
};

const ModalFooter = ({ children, className }: { children: ReactNode; className?: string }) => {
  return (
    <div className={`p-4 border-t bg-gray-50 rounded-b-lg ${className || ''}`}>
      {children}
    </div>
  );
};

// Attach compound components
Modal.Content = ModalContent;
Modal.Header = ModalHeader;
Modal.Body = ModalBody;
Modal.Footer = ModalFooter;

// ===== PERFORMANCE OPTIMIZED BUTTON =====

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'success' | 'danger' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  isLoading?: boolean;
  isDisabled?: boolean;
  fullWidth?: boolean;
  children: ReactNode;
  onClick?: () => void;
  className?: string;
}

// Pre-compile button classes for performance
const buttonClassGenerator = createButtonClasses();

const Button = memo<ButtonProps>(({
  variant = 'primary',
  size = 'medium',
  isLoading = false,
  isDisabled = false,
  fullWidth = false,
  children,
  onClick,
  className
}) => {
  const buttonClass = buttonClassGenerator(variant, [
    size,
    isLoading && 'loading',
    isDisabled && 'disabled',
    fullWidth && 'fullWidth'
  ].filter(Boolean));
  
  const handleClick = useCallback(() => {
    if (!isLoading && !isDisabled) {
      onClick?.();
    }
  }, [onClick, isLoading, isDisabled]);
  
  return (
    <button
      className={`${buttonClass} ${className || ''}`}
      onClick={handleClick}
      disabled={isLoading || isDisabled}
    >
      {isLoading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      {children}
    </button>
  );
});

Button.displayName = 'Button';

// ===== EXAMPLE USAGE =====

// Example of composed component with all patterns
const ExampleUserManagementPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  
  const sampleUsers: User[] = [
    { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin', isActive: true, lastLogin: new Date() },
    { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'user', isActive: true, lastLogin: new Date() },
    { id: '3', name: 'Bob Johnson', email: 'bob@example.com', role: 'user', isActive: false }
  ];
  
  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">User Management</h1>
        <Button onClick={() => setIsModalOpen(true)}>
          Add User
        </Button>
      </div>
      
      <UserList
        users={sampleUsers}
        variant="detailed"
        showEmail={true}
        onUserAction={(action) => console.log('User action:', action)}
      />
      
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      >
        <Modal.Content>
          <Modal.Header>
            <h2 className="text-xl font-semibold">Add New User</h2>
          </Modal.Header>
          <Modal.Body>
            <p>User form would go here...</p>
          </Modal.Body>
          <Modal.Footer>
            <div className="flex justify-end space-x-2">
              <Button variant="ghost" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button variant="primary">
                Save User
              </Button>
            </div>
          </Modal.Footer>
        </Modal.Content>
      </Modal>
    </div>
  );
};

export {
  useUserManagement,
  useForm,
  UserCardPure,
  UserList,
  Modal,
  Button,
  ExampleUserManagementPage
};

export default {
  useUserManagement,
  useForm,
  UserCardPure,
  UserList,
  Modal,
  Button,
  ExampleUserManagementPage
};