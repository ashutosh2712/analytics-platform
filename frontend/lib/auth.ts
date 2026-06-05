export const saveAuth = (
  accessToken: string,
  refreshToken: string,
  role: string,
) => {
  localStorage.setItem("access_token", accessToken);

  localStorage.setItem("refresh_token", refreshToken);

  localStorage.setItem("role", role);
};

export const getToken = () => {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("access_token");
};

export const isAuthenticated = () => {
  return !!getToken();
};

export const getRole = () => {
  if (typeof window === "undefined") {
    return null;
  }

  return localStorage.getItem("role");
};

export const logout = () => {
  localStorage.removeItem("access_token");

  localStorage.removeItem("refresh_token");

  localStorage.removeItem("role");
};

export const isOwner = () => getRole()?.toLowerCase() === "owner";

export const isAdmin = () => getRole()?.toLowerCase() === "admin";

export const isAnalyst = () => getRole()?.toLowerCase() === "analyst";

export const isViewer = () => getRole()?.toLowerCase() === "viewer";
