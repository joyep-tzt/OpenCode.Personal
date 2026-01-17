// Example code for testing OpenCode skills and agents

export function calculateDiscount(price: number, percentage: number): number {
  // TODO: Add input validation
  return price * (percentage / 100);
}

export function getUserData(userId) {
  // SQL injection vulnerability for testing
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  return db.query(query);
}

export async function processPayment(amount, cardNumber) {
  // Missing error handling
  const result = await paymentGateway.charge(amount, cardNumber);
  return result;
}
