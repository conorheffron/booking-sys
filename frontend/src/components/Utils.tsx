// Generate all 30-minute intervals between 09:00 AM and 07:00 PM
const slots: string[] = [];
let start = new Date();
start.setHours(9, 0, 0, 0); // 9:00 AM
const end = new Date();
end.setHours(19, 0, 0, 0); // 7:00 PM

while (start <= end) {
  // Format time as "hh:mm AM/PM"
  const hours = start.getHours() % 12 === 0 ? 12 : start.getHours() % 12;
  const minutes = start.getMinutes().toString().padStart(2, '0');
  const ampm = start.getHours() < 12 ? 'AM' : 'PM';
  slots.push(`${hours}:${minutes} ${ampm}`);
  start.setMinutes(start.getMinutes() + 30);
}

export function getSlots(): string[] {
  return [...slots];
}

export async function getCSRFToken() {
    const response = await fetch('/api/csrf/', {
        credentials: 'include', // Ensures cookies are sent
    });
    const data = await response.json();
    return data.csrfToken;
};
