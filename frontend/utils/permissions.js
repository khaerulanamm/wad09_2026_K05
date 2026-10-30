export function canManage(ownerId, user) {
  return Boolean(user && (user.role === 'admin' || user.id === ownerId))
}
