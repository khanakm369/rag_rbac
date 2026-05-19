import React, { useEffect } from "react"
import { useNavigate } from "react-router-dom"

const Signout = () => {
  const navigate = useNavigate()

  useEffect(() => {
    // 🧹 remove token
    localStorage.removeItem("token")

    // 🔁 redirect to signin
    navigate("/signin")
  }, [navigate])

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Logging out...</h2>
    </div>
  )
}

export default Signout