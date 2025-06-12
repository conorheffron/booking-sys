// Hardcoded slots
const slots = [
  '09:00 AM', '10:00 AM', '11:00 AM', '12:00 PM',
  '01:00 PM', '02:00 PM', '03:00 PM', '04:00 PM',
  '04:30 PM', '05:00 PM', '05:30 PM', '06:00 PM',
  '06:30 PM', '07:00 PM'
];
  
export function getSlots(): string[] {
  return slots;
}

export async function getCSRFToken() {
    const response = await fetch('/api/csrf/', {
        credentials: 'include', // Ensures cookies are sent
    });
    const data = await response.json();
    return data.csrfToken;
};
