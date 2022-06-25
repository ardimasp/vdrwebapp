import { encryptToken } from "../function";

class TokenService {
    setUser(user) {
      localStorage.setItem("user", encryptToken(user));
    }
    removeUser() {
      localStorage.removeItem("user");
      localStorage.removeItem("profile");
    }
  }
  export default new TokenService();