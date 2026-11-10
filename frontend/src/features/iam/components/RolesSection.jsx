import { Button } from "../../../shared/ui/Button";
import { Input } from "../../../shared/ui/Input";

export function RolesSection({
  searchQuery,
  onSearchQueryChange,
  page,
  totalPages,
  totalItems,
  onPrevPage,
  onNextPage,
  roleName,
  setRoleName,
  roleDescription,
  setRoleDescription,
  rolePermissionIds,
  setRolePermissionIds,
  onCreate,
  isCreating,
  roles,
  onDelete,
}) {
  return (
    <section className="card iam-card">
      <h2>Roles</h2>
      <p className="iam-hint">Permission IDs (comma separated).</p>
      <Input
        placeholder="search roles..."
        value={searchQuery}
        onChange={(event) => onSearchQueryChange(event.target.value)}
        data-testid="input-role-search"
      />
      <Input
        placeholder="role name"
        value={roleName}
        onChange={(event) => setRoleName(event.target.value)}
        data-testid="input-role-name"
      />
      <Input
        placeholder="description (opsional)"
        value={roleDescription}
        onChange={(event) => setRoleDescription(event.target.value)}
        data-testid="input-role-description"
      />
      <Input
        placeholder="permission IDs, pisahkan koma"
        value={rolePermissionIds}
        onChange={(event) => setRolePermissionIds(event.target.value)}
        data-testid="input-role-permission-ids"
      />
      <Button
        variant="success"
        onClick={onCreate}
        disabled={!roleName || isCreating}
        data-testid="btn-create-role"
      >
        Create Role
      </Button>
      <div className="iam-pagination" data-testid="pager-roles">
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
        {roles.map((role) => (
          <li className="iam-row" key={role.id}>
            <div>
              <strong>{role.name}</strong>
              <div className="iam-meta">{role.id}</div>
              <div className="iam-meta">
                {role.permissions?.map((permission) => permission.code).join(", ") || "-"}
              </div>
            </div>
            <Button
              variant="danger"
              className="btn-sm"
              onClick={() => onDelete(role.id)}
              data-testid={`btn-delete-role-${role.id}`}
            >
              Delete
            </Button>
          </li>
        ))}
      </ul>
    </section>
  );
}
