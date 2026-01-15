package utils

// Vector represents a 2D vector
type Vector struct {
	X int
	Y int
}

type Position Vector

// Add returns the sum of two vectors
func (v Vector) Add(other Vector) Vector {
	return Vector{X: v.X + other.X, Y: v.Y + other.Y}
}

// Subtract returns the difference between two vectors
func (v Vector) Subtract(other Vector) Vector {
	return Vector{X: v.X - other.X, Y: v.Y - other.Y}
}

// Multiply scales a vector by a scalar
func (v Vector) Multiply(scalar int) Vector {
	return Vector{X: v.X * scalar, Y: v.Y * scalar}
}

// Divide scales a vector by a scalar
func (v Vector) Divide(scalar int) Vector {
	return Vector{X: v.X / scalar, Y: v.Y / scalar}
}
