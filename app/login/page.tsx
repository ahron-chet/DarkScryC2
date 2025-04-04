"use client";
import { useState } from "react";
import { signIn } from "next-auth/react";
import { useRouter ,useSearchParams} from "next/navigation";
import Script from 'next/script';
import "bootstrap/dist/css/bootstrap.min.css";
import "./login.css";


export default function LoginPage() {

  const searchParams = useSearchParams();

  // If the user was redirected to /login?callbackUrl=...
  // NextAuth sets that so we know where to go after successful sign in
  const callbackUrl = searchParams.get("callbackUrl") || "/";
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e:any) {
    e.preventDefault();
    setMessage("");
    setIsLoading(true);
    const result = await signIn("credentials", {
      username,
      password,
      redirect: false,
      callbackUrl,
    });

    setIsLoading(false);
    if (result?.ok) {
      // Successful login
      router.push(result.url || callbackUrl);
    } else {
      // Failed login
      setMessage("Invalid credentials or server error");
    }
  }

  return (
    <>
      <Script
        src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r121/three.min.js"
        strategy="beforeInteractive"
      />
      <Script
        src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"
        strategy="beforeInteractive"
      />

      <Script id="init-vanta" strategy="afterInteractive">
        {`
          if (window.VANTA && window.VANTA.NET) {
            window.VANTA.NET({
              el: "#vanta-bg",
              mouseControls: false,
              touchControls: true,
              gyroControls: false,
              color: 0xffffff,
              color2: 0x497ea5,
              backgroundColor: 0x10131a,
              points: 12.0,
              maxDistance: 20.0,
              spacing: 17.0
            });
          }
        `}
      </Script>
    <div style={{ margin: 0, padding: 0, overflow: "hidden" }}>
      <div id="vanta-bg" />
      <div className="login-wrapper">
        <div className="login-card">
          <div className="row g-0">
            <div className="col-12 col-lg-6 brand-col mb-4 mb-lg-0">
              <img
                src="/images/logo.png"
                alt="DarkSCRY Logo"
                style={{ marginLeft: "auto", marginRight: "auto" }}
              />
              <p style={{ textAlign: "center" }}>
                Empowering Intelligence with Cutting-Edge Analysis.
                Discover insights that matter most to your digital world.
              </p>
            </div>

            <div className="col-12 col-lg-6 form-col" style={{ alignItems: "center" }}>
              <h1>Welcome. Please Log In.</h1>
              <form
                onSubmit={handleSubmit}
                className="w-100"
                style={{ maxWidth: "400px" }}
              >
                <div className="form-floating mb-3">
                  <input
                    type="text"
                    className="form-control"
                    placeholder="Email or Username"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                  <label htmlFor="floatingEmail">
                    <svg 
                      xmlns="http://www.w3.org/2000/svg"
                      width="16" 
                      height="16" 
                      fill="currentColor"
                      className="bi bi-person-circle me-2" 
                      viewBox="0 0 16 16"
                    >
                      <path d="M13.468 12.37C12.758 11.226 11.168 10.5 8 
                              10.5c-3.168 0-4.758.726-5.468 1.87A6.972 
                              6.972 0 0 0 8 14a6.972 6.972 0 0 0 
                              5.468-1.63z"/>
                      <path fillRule="evenodd" 
                            d="M8 9a3 3 0 1 0 
                              0-6 3 3 0 0 0 0 6z"/>
                      <path fillRule="evenodd" 
                            d="M8 1a7 7 0 1 0 
                              0 14A7 7 0 0 0 8 1z"/>
                    </svg>
                    Email / Username
                  </label>
                </div>

                <div className="form-floating mb-3">
                  <input
                    type="password"
                    className="form-control"
                    placeholder="Password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                  <label htmlFor="floatingPassword">
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    width="16" 
                    height="16" 
                    fill="currentColor" 
                    className="bi bi-lock-fill me-2" 
                    viewBox="0 0 16 16"
                  >
                    <path d="M8 1a3 3 0 0 
                            0-3 3v2h6V4a3 3 0 0 0-3-3z"/>
                    <path d="M3 8a2 2 0 0 1 
                            2-2h6a2 2 0 0 1 2 
                            2v5a2 2 0 0 1-2 
                            2H5a2 2 0 0 1-2-2V8z"/>
                  </svg>
                  Password
                </label>
                </div>

                <button type="submit" className="btn btn-custom w-100 py-2 mb-3">
                  Login
                </button>

                <div id="loadingSpinner" className="d-flex justify-content-center my-3">
                  {isLoading && (
                    <div className="spinner-border text-light" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                </div>

                <div
                  id="loginMessage"
                  className="mt-2 text-center"
                  style={{ whiteSpace: "pre-wrap", color: "red" }}
                >
                  {message}
                </div>

                <div className="d-flex justify-content-between mt-3">
                  <a href="#" className="text-decoration-none text-white-50">
                    Need Help?
                  </a>
                  <a href="#" className="text-decoration-none text-white-50">
                    Forgot Password?
                  </a>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
    </>
  );
}
