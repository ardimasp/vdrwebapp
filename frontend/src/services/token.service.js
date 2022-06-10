import { encryptToken } from "../function";

class TokenService {
    getLocalRefreshToken() {
      const user = localStorage.getItem("user");
      return user;
    }
    getLocalAccessToken() {
      const user = localStorage.getItem("user");
      // decryptToken(user)
      return user;
    }
    updateLocalAccessToken(token) {
      let user = localStorage.getItem("user");
      user.accessToken = token;
      localStorage.setItem("user", user);
    }
    getUser() {
      return localStorage.getItem("user");
    }
    setUser(user) {
      localStorage.setItem("user", user);
      console.log("set local user", encryptToken(user))
    }
    removeUser() {
      localStorage.removeItem("user");
      localStorage.removeItem("username");
      localStorage.removeItem("type");
      localStorage.removeItem("profile");
    }
  }
  export default new TokenService();