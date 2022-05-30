class TokenService {
    getLocalRefreshToken() {
      const user = localStorage.getItem("user");
      return user;
    }
    getLocalAccessToken() {
      const user = localStorage.getItem("user");
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
      console.log(user);
      localStorage.setItem("user", user);
    }
    removeUser() {
      localStorage.removeItem("user");
      localStorage.removeItem("username");
      localStorage.removeItem("type");
    }
  }
  export default new TokenService();