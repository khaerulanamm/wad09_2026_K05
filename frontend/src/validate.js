// F3: aturan yang sama dengan skema Pydantic di backend (backend/app/schemas.py).
// Validasi klien memberi umpan balik cepat; backend tetap memvalidasi karena klien bisa dilewati.

export const LEVELS = [
  { value: 'beginner', label: 'Pemula' },
  { value: 'intermediate', label: 'Menengah' },
  { value: 'advanced', label: 'Lanjutan' },
]

const TIME_PATTERN = /^([01]\d|2[0-3]):[0-5]\d$/

export function emptySession() {
  return {
    class_name: '',
    instructor: '',
    date: '',
    start_time: '',
    duration_min: 60,
    capacity: 20,
    level: 'beginner',
  }
}

function inRange(value, min, max) {
  return Number.isInteger(value) && value >= min && value <= max
}

export function validateSession(form) {
  const errors = {}
  const name = form.class_name.trim()
  const instructor = form.instructor.trim()
  if (!name) errors.class_name = 'Nama kelas wajib diisi.'
  else if (name.length > 60) errors.class_name = 'Nama kelas maksimal 60 karakter.'
  if (!instructor) errors.instructor = 'Nama instruktur wajib diisi.'
  else if (instructor.length > 60) errors.instructor = 'Nama instruktur maksimal 60 karakter.'
  if (!form.date) errors.date = 'Tanggal wajib diisi.'
  if (!TIME_PATTERN.test(form.start_time)) errors.start_time = 'Jam mulai wajib diisi (JJ:MM).'
  if (!inRange(form.duration_min, 15, 180)) errors.duration_min = 'Durasi harus 15–180 menit.'
  if (!inRange(form.capacity, 1, 50)) errors.capacity = 'Kapasitas harus 1–50 orang.'
  if (!LEVELS.some((l) => l.value === form.level)) errors.level = 'Pilih level kelas.'
  return errors
}

// Balasan 422 FastAPI berbentuk [{ loc: ['body', 'nama_field'], msg: '...' }].
// Ubah menjadi { nama_field: pesan } supaya tampil di bawah input yang bersangkutan.
export function serverFieldErrors(err) {
  if (err.status !== 422 || !Array.isArray(err.detail)) return {}
  const errors = {}
  for (const item of err.detail) {
    const field = item.loc?.at(-1)
    if (typeof field === 'string') errors[field] = item.msg
  }
  return errors
}
