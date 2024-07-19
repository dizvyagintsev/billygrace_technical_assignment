import PropTypes from "prop-types";
import {
  createContext,
  useEffect,
  useReducer,
  useCallback,
  useMemo,
} from "react";

// ----------------------------------------------------------------------

const initialState = {
  isInitialized: false,
  isAuthenticated: false,
  user: null,
};

const credentials = {
  email: "demo@minimals.cc",
  password: "demo1234",
};

const demoUser = {
  email: credentials.email,
  displayName: "Demo User",
  role: "user for demo",
  customerId: "23",
};

const reducer = (state, action) => {
  switch (action.type) {
    case "INITIAL":
      return {
        isInitialized: true,
        isAuthenticated: action.payload.isAuthenticated,
        user: action.payload.user,
      };
    case "LOGIN":
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload.user,
      };
    case "LOGOUT":
      return {
        ...state,
        isAuthenticated: false,
        user: null,
      };
    default:
      return state;
  }
};

// ----------------------------------------------------------------------

export const AuthContext = createContext(null);

// ----------------------------------------------------------------------

AuthProvider.propTypes = {
  children: PropTypes.node,
};

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const initialize = useCallback(() => {
    // Check local storage for previous login state
    const isAuthenticated = localStorage.getItem("isAuthenticated") === "true";
    const user = isAuthenticated ? demoUser : null;

    dispatch({
      type: "INITIAL",
      payload: {
        isAuthenticated,
        user,
      },
    });
  }, []);

  useEffect(() => {
    initialize();
  }, [initialize]);

  // LOGIN
  const login = useCallback((email, password) => {
    if (email === credentials.email && password === credentials.password) {
      const user = demoUser;

      // Save login state to local storage
      localStorage.setItem("isAuthenticated", "true");

      dispatch({
        type: "LOGIN",
        payload: {
          user,
        },
      });
    } else {
      throw new Error("Invalid email or password");
    }
  }, []);

  // LOGOUT
  const logout = useCallback(() => {
    // Clear login state from local storage
    localStorage.removeItem("isAuthenticated");

    dispatch({
      type: "LOGOUT",
    });
  }, []);

  const memoizedValue = useMemo(
    () => ({
      isInitialized: state.isInitialized,
      isAuthenticated: state.isAuthenticated,
      user: state.user,
      login,
      logout,
    }),
    [state.isAuthenticated, state.isInitialized, state.user, login, logout]
  );

  return (
    <AuthContext.Provider value={memoizedValue}>
      {children}
    </AuthContext.Provider>
  );
}
