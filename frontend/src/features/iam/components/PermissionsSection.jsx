import { Button } from "../../../shared/ui/Button";
import { Input } from "../../../shared/ui/Input";

export function PermissionsSection({
  permissionCodesHint,
  searchQuery,
  onSearchQueryChange,
  page,
  totalPages,
  totalItems,
  onPrevPage,
  onNextPage,
  permissionCode,
  setPermissionCode,
  permissionDescription,
  setPermissionDescription,
  onCreate,
  isCreating,
  permissions,
  onDelete,
}) {
  return (
    <section className="card iam-card">
      <h2>Permissions</h2>
      <p className="iam-hint">ID reference: {permissionCodesHint}</p>
      <Input
        placeholder="search permissions..."
        value={searchQuery}
        onChange={(event) => onSearchQueryChange(event.target.value)}
        data-testid="input-permission-search"
      />
      <Input
        placeholder="permission code (contoh: orders.read)"
        value={permissionCode}
        onChange={(event) => setPermissionCode(event.target.value)}
        data-testid="input-permission-code"
      />
      <Input
        placeholder="description (opsional)"
        value={permissionDescription}
        onChange={(event) => setPermissionDescription(event.target.value)}
        data-testid="input-permission-description"
      />
      <Button
        variant="success"
        onClick={onCreate}
        disabled={!permissionCode || isCreating}
        data-testid="btn-create-permission"
      >
        Create Permission
      </Button>
      <div className="iam-pagination" data-testid="pager-permissions">
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
        {permissions.map((permission) => (
          <li className="iam-row" key={permission.id}>
            <div>
              <strong>{permission.code}</strong>
              <div className="iam-meta">{permission.id}</div>
            </div>
            <Button
              variant="danger"
              className="btn-sm"
              onClick={() => onDelete(permission.id)}
              data-testid={`btn-delete-permission-${permission.id}`}
            >
              Delete
            </Button>
          </li>
        ))}
      </ul>
    </section>
  );
}
