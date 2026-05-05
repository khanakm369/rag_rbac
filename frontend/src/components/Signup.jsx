import React, { useState, useEffect } from 'react'

const Signup = () => {

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    role: ''
  })

  const [roles, setRoles] = useState([])

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  // 🔥 Fetch roles from backend
  useEffect(() => {
    const fetchRoles = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/roles")
        const data = await res.json()
        setRoles(data.roles)
      } catch (err) {
        console.error("Error fetching roles", err)
      }
    }

    fetchRoles()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match")
      return
    }

    if (!formData.role) {
      alert("Please select a role")
      return
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"  // ✅ FIXED
        },
        body: JSON.stringify({
          username: formData.email,
          password: formData.password,
          role: formData.role
        })
      })

      const data = await response.json()

      if (!response.ok) {
        alert(data.detail || "Something went wrong")
        return
      }

      alert("User created successfully ✅")
      console.log(data)

    } catch (err) {
      console.error(err)
      alert("Server error")
    }
  }

  return (
    <div>
      <form
        style={{ display: "grid", gap: "10px", justifyContent: "center", alignItems: "center" }}
        onSubmit={handleSubmit}
      >
        <h2>Sign Up</h2>

        <input
          type='email'
          name='email'
          placeholder='Enter your email'
          onChange={handleChange}
        />

        <input
          type='password'
          name='password'
          placeholder='Enter your Password'
          onChange={handleChange}
        />

        <input
          type='password'
          name='confirmPassword'
          placeholder='Re-enter your password'
          onChange={handleChange}
        />

        {/* 🔥 Dynamic roles from DB */}
        <select name='role' onChange={handleChange}>
          <option value="">Select Role</option>
          {roles.map((role, index) => (
            <option key={index} value={role}>
              {role}
            </option>
          ))}
        </select>

        <button type="submit">Signup</button>
      </form>
    </div>
  )
}

export default Signup