import React, { useState } from "react"
import { useNavigate } from "react-router-dom"

const Signin = () => {
  const navigate = useNavigate()

  const [formData, setFormData] = useState({
    username: "",
    password: ""
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const res = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      })

      const data = await res.json()

      if (!res.ok) {
        alert(data.detail || "Login failed")
        return
      }

      // ✅ Save token
      localStorage.setItem("token", data.access_token)

      // ✅ Redirect after login
      navigate("/promt")

    } catch (err) {
      console.error(err)
      alert("Server error")
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "10px", width: "300px", margin: "auto" }}>
        <h2>Sign In</h2>

        <input
          type="text"
          name="username"
          placeholder="Enter username"
          onChange={handleChange}
        />

        <input
          type="password"
          name="password"
          placeholder="Enter password"
          onChange={handleChange}
        />

        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default Signin