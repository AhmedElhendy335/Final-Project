const API_URL = 'http://localhost:3000';

// Add Student
document.getElementById('add-student-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const student = {
    student_id: document.getElementById('student-id').value,
    name: document.getElementById('student-name').value,
    nickname: document.getElementById('student-nickname').value,
    age: document.getElementById('student-age').value,
    grade: document.getElementById('student-grade').value,
    registration_date: document.getElementById('registration-date').value,
  };

  const lessons = document.getElementById('student-lessons').value.split(',');

  const response = await fetch(`${API_URL}/add-student`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student, lessons }),
  });

  const data = await response.json();
  alert(data.message || data.error);
});

// Delete Student
document.getElementById('delete-student-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const studentId = document.getElementById('delete-student-id').value;

  const response = await fetch(`${API_URL}/delete-student/${studentId}`, { method: 'DELETE' });
  const data = await response.json();
  alert(data.message || data.error);
});

// Update Student
document.getElementById('update-student-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const studentId = document.getElementById('update-student-id').value;
  const updatedInfo = {
    name: document.getElementById('update-student-name').value,
    nickname: document.getElementById('update-student-nickname').value,
    age: document.getElementById('update-student-age').value,
    grade: document.getElementById('update-student-grade').value,
    registration_date: document.getElementById('update-registration-date').value,
  };

  const response = await fetch(`${API_URL}/update-student/${studentId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updatedInfo),
  });

  const data = await response.json();
  alert(data.message || data.error);
});

// Show Student Info
document.getElementById('show-student-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const studentId = document.getElementById('show-student-id').value;

  const response = await fetch(`${API_URL}/show-student/${studentId}`);
  const data = await response.json();

  const infoDiv = document.getElementById('student-info');
  if (data.error) {
    infoDiv.innerText = data.error;
  } else {
    infoDiv.innerText = `
      Name: ${data.student.name}
      Nickname: ${data.student.nickname}
      Age: ${data.student.age}
      Grade: ${data.student.grade}
      Registration Date: ${data.student.registration_date}
      Lessons: ${data.lessons.join(', ')}
    `;
  }
});
