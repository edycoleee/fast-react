import { Button } from "../../../shared/ui/Button";
import { Input } from "../../../shared/ui/Input";

export function UsersSection({
  roleNamesHint,
  searchQuery,
  onSearchQueryChange,
  activeFilter,
  onActiveFilterChange,
  page,
  totalPages,
  totalItems,
  onPrevPage,
  onNextPage,
  username,
  setUsername,
  email,
  setEmail,
  password,
  setPassword,
  userRoleIds,
  setUserRoleIds,
  onCreate,
  isCreating,
  users,
  onToggleStatus,
  onDelete,
}) {
  return (
    <section className="card iam-card">
      <h2>Users</h2>
      <p className="iam-hint">Role IDs (comma separated). Current roles: {roleNamesHint}</p>
      <Input
        placeholder="search users..."
        value={searchQuery}
        onChange={(event) => onSearchQueryChange(event.target.value)}
        data-testid="input-user-search"
      />
      <select
        className="input"
        value={activeFilter}
        onChange={(event) => onActiveFilterChange(event.target.value)}
        data-testid="select-user-active-filter"
      >
        <option value="all">All statuses</option>
        <option value="active">Active only</option>
        <option value="inactive">Inactive only</option>
      </select>
      <Input
        placeholder="username"
        value={username}
        onChange={(event) => setUsername(event.target.value)}
        data-testid="input-user-username"
      />
      <Input
        placeholder="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        data-testid="input-user-email"
      />
      <Input
        placeholder="password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        data-testid="input-user-password"
      />
      <Input
        placeholder="role IDs, pisahkan koma"
        value={userRoleIds}
        onChange={(event) => setUserRoleIds(event.target.value)}
        data-testid="input-user-role-ids"
      />
      <Button
        variant="success"
        onClick={onCreate}
        disabled={!username || !email || !password || isCreating}
        data-testid="btn-create-user"
      >
        Create User
      </Button>
      <div className="iam-pagination" data-testid="pager-users">
        <Button
          variant="outline"
          className="btn-sm"
          onClick={onPrevPage}
          disabled={page <= 1}
        >
          Prev
        </Button>
        <span className="iam-meta">
          Page {page}/{totalPages} · {totalItems} items
        </span>
        <Button
          variant="outline"
          className="btn-sm"
          onClick={onNextPage}
          disabled={page >= totalPages}
        >
          Next
        </Button>
      </div>
      <ul className="iam-list">
        {users.map((user) => (
          <li className="iam-row" key={user.id}>
            <div>
              <strong>{user.username}</strong> ({user.email})
              <div className="iam-meta">
                Status: {user.is_active ? "active" : "inactive"} · roles:{" "}
                {user.roles?.map((role) => role.name).join(", ") || "-"}
              </div>
            </div>
            <div className="iam-actions">
              <Button
                variant="outline"
                className="btn-sm"
                onClick={() => onToggleStatus(user.id, user.is_active)}
                data-testid={`btn-toggle-user-${user.id}`}
              >
                Toggle Active
              </Button>
              <Button
                variant="danger"
                className="btn-sm"
                onClick={() => onDelete(user.id)}
                data-testid={`btn-delete-user-${user.id}`}
              >
                Delete
              </Button>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
