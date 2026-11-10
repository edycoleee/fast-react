import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "../../api/client";
import { PermissionsSection } from "../../features/iam/components/PermissionsSection";
import { RolesSection } from "../../features/iam/components/RolesSection";
import { UsersSection } from "../../features/iam/components/UsersSection";

const splitCsv = (rawValue) =>
  rawValue
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

const getErrorMessage = (error, fallbackMessage) =>
  error?.response?.data?.detail || error?.response?.data?.message || fallbackMessage;

const PAGE_SIZE = 5;

export function AdminAccessPage() {
  const queryClient = useQueryClient();
  const [permissionCode, setPermissionCode] = useState("");
  const [permissionDescription, setPermissionDescription] = useState("");
  const [roleName, setRoleName] = useState("");
  const [roleDescription, setRoleDescription] = useState("");
  const [rolePermissionIds, setRolePermissionIds] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userRoleIds, setUserRoleIds] = useState("");
  const [permissionSearchQuery, setPermissionSearchQuery] = useState("");
  const [roleSearchQuery, setRoleSearchQuery] = useState("");
  const [userSearchQuery, setUserSearchQuery] = useState("");
  const [userActiveFilter, setUserActiveFilter] = useState("all");
  const [permissionPage, setPermissionPage] = useState(1);
  const [rolePage, setRolePage] = useState(1);
  const [userPage, setUserPage] = useState(1);
  const [feedback, setFeedback] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const invalidateAll = () =>
    Promise.all([
      queryClient.invalidateQueries({ queryKey: ["iam-permissions"] }),
      queryClient.invalidateQueries({ queryKey: ["iam-roles"] }),
      queryClient.invalidateQueries({ queryKey: ["iam-users"] }),
    ]);

  const permissionsQuery = useQuery({
    queryKey: ["iam-permissions", permissionSearchQuery, permissionPage],
    queryFn: async () => {
      const response = await apiClient.get("/iam/permissions", {
        params: { q: permissionSearchQuery || undefined, page: permissionPage, page_size: PAGE_SIZE },
      });
      return response.data;
    },
  });

  const rolesQuery = useQuery({
    queryKey: ["iam-roles", roleSearchQuery, rolePage],
    queryFn: async () => {
      const response = await apiClient.get("/iam/roles", {
        params: { q: roleSearchQuery || undefined, page: rolePage, page_size: PAGE_SIZE },
      });
      return response.data;
    },
  });

  const usersQuery = useQuery({
    queryKey: ["iam-users", userSearchQuery, userPage, userActiveFilter],
    queryFn: async () => {
      const response = await apiClient.get("/iam/users", {
        params: {
          q: userSearchQuery || undefined,
          page: userPage,
          page_size: PAGE_SIZE,
          is_active:
            userActiveFilter === "all" ? undefined : userActiveFilter === "active",
        },
      });
      return response.data;
    },
  });

  const loading =
    permissionsQuery.isLoading || rolesQuery.isLoading || usersQuery.isLoading;

  const onSuccess = async (message) => {
    setErrorMessage("");
    setFeedback(message);
    await invalidateAll();
  };

  const onError = (error, fallbackMessage) => {
    setFeedback("");
    setErrorMessage(getErrorMessage(error, fallbackMessage));
  };

  const createPermissionMutation = useMutation({
    mutationFn: async () =>
      apiClient.post("/iam/permissions", {
        code: permissionCode,
        description: permissionDescription || null,
      }),
    onSuccess: async () => {
      setPermissionCode("");
      setPermissionDescription("");
      await onSuccess("Permission created.");
    },
    onError: (error) => onError(error, "Failed to create permission."),
  });

  const deletePermissionMutation = useMutation({
    mutationFn: async (permissionId) => apiClient.delete(`/iam/permissions/${permissionId}`),
    onSuccess: async () => onSuccess("Permission deleted."),
    onError: (error) => onError(error, "Failed to delete permission."),
  });

  const createRoleMutation = useMutation({
    mutationFn: async () =>
      apiClient.post("/iam/roles", {
        name: roleName,
        description: roleDescription || null,
        permission_ids: splitCsv(rolePermissionIds),
      }),
    onSuccess: async () => {
      setRoleName("");
      setRoleDescription("");
      setRolePermissionIds("");
      await onSuccess("Role created.");
    },
    onError: (error) => onError(error, "Failed to create role."),
  });

  const deleteRoleMutation = useMutation({
    mutationFn: async (roleId) => apiClient.delete(`/iam/roles/${roleId}`),
    onSuccess: async () => onSuccess("Role deleted."),
    onError: (error) => onError(error, "Failed to delete role."),
  });

  const createUserMutation = useMutation({
    mutationFn: async () =>
      apiClient.post("/iam/users", {
        username,
        email,
        password,
        role_ids: splitCsv(userRoleIds),
        is_active: true,
      }),
    onSuccess: async () => {
      setUsername("");
      setEmail("");
      setPassword("");
      setUserRoleIds("");
      await onSuccess("User created.");
    },
    onError: (error) => onError(error, "Failed to create user."),
  });

  const toggleUserStatusMutation = useMutation({
    mutationFn: async ({ userId, isActive }) =>
      apiClient.patch(`/iam/users/${userId}`, { is_active: !isActive }),
    onSuccess: async () => onSuccess("User status updated."),
    onError: (error) => onError(error, "Failed to update user status."),
  });

  const deleteUserMutation = useMutation({
    mutationFn: async (userId) => apiClient.delete(`/iam/users/${userId}`),
    onSuccess: async () => onSuccess("User deleted."),
    onError: (error) => onError(error, "Failed to delete user."),
  });

  const permissionCodesHint = useMemo(
    () => permissionsQuery.data?.data?.map((item) => `${item.code} (${item.id})`).join(", ") || "-",
    [permissionsQuery.data]
  );

  const roleNamesHint = useMemo(
    () => rolesQuery.data?.data?.map((item) => `${item.name} (${item.id})`).join(", ") || "-",
    [rolesQuery.data]
  );

  return (
    <main className="container" data-testid="page-admin-access">
      <h1>Access Management</h1>
      <p>Kelola permission, role, dan user untuk boilerplate turunan.</p>
      {feedback ? (
        <p className="message-success" data-testid="success-admin-access">
          {feedback}
        </p>
      ) : null}
      {errorMessage ? (
        <p className="message-error" data-testid="error-admin-access">
          {errorMessage}
        </p>
      ) : null}
      {loading ? <p data-testid="loading-admin-access">Loading...</p> : null}

      <div className="iam-grid">
        <PermissionsSection
          permissionCodesHint={permissionCodesHint}
          searchQuery={permissionSearchQuery}
          onSearchQueryChange={(value) => {
            setPermissionSearchQuery(value);
            setPermissionPage(1);
          }}
          page={permissionsQuery.data?.meta?.page || 1}
          totalPages={permissionsQuery.data?.meta?.total_pages || 1}
          totalItems={permissionsQuery.data?.meta?.total || 0}
          onPrevPage={() => setPermissionPage((currentPage) => Math.max(1, currentPage - 1))}
          onNextPage={() =>
            setPermissionPage((currentPage) =>
              Math.min(permissionsQuery.data?.meta?.total_pages || 1, currentPage + 1)
            )
          }
          permissionCode={permissionCode}
          setPermissionCode={setPermissionCode}
          permissionDescription={permissionDescription}
          setPermissionDescription={setPermissionDescription}
          onCreate={() => createPermissionMutation.mutate()}
          isCreating={createPermissionMutation.isPending}
          permissions={permissionsQuery.data?.data || []}
          onDelete={(permissionId) => deletePermissionMutation.mutate(permissionId)}
        />

        <RolesSection
          searchQuery={roleSearchQuery}
          onSearchQueryChange={(value) => {
            setRoleSearchQuery(value);
            setRolePage(1);
          }}
          page={rolesQuery.data?.meta?.page || 1}
          totalPages={rolesQuery.data?.meta?.total_pages || 1}
          totalItems={rolesQuery.data?.meta?.total || 0}
          onPrevPage={() => setRolePage((currentPage) => Math.max(1, currentPage - 1))}
          onNextPage={() =>
            setRolePage((currentPage) =>
              Math.min(rolesQuery.data?.meta?.total_pages || 1, currentPage + 1)
            )
          }
          roleName={roleName}
          setRoleName={setRoleName}
          roleDescription={roleDescription}
          setRoleDescription={setRoleDescription}
          rolePermissionIds={rolePermissionIds}
          setRolePermissionIds={setRolePermissionIds}
          onCreate={() => createRoleMutation.mutate()}
          isCreating={createRoleMutation.isPending}
          roles={rolesQuery.data?.data || []}
          onDelete={(roleId) => deleteRoleMutation.mutate(roleId)}
        />

        <UsersSection
          roleNamesHint={roleNamesHint}
          searchQuery={userSearchQuery}
          onSearchQueryChange={(value) => {
            setUserSearchQuery(value);
            setUserPage(1);
          }}
          activeFilter={userActiveFilter}
          onActiveFilterChange={(value) => {
            setUserActiveFilter(value);
            setUserPage(1);
          }}
          page={usersQuery.data?.meta?.page || 1}
          totalPages={usersQuery.data?.meta?.total_pages || 1}
          totalItems={usersQuery.data?.meta?.total || 0}
          onPrevPage={() => setUserPage((currentPage) => Math.max(1, currentPage - 1))}
          onNextPage={() =>
            setUserPage((currentPage) =>
              Math.min(usersQuery.data?.meta?.total_pages || 1, currentPage + 1)
            )
          }
          username={username}
          setUsername={setUsername}
          email={email}
          setEmail={setEmail}
          password={password}
          setPassword={setPassword}
          userRoleIds={userRoleIds}
          setUserRoleIds={setUserRoleIds}
          onCreate={() => createUserMutation.mutate()}
          isCreating={createUserMutation.isPending}
          users={usersQuery.data?.data || []}
          onToggleStatus={(userId, isActive) =>
            toggleUserStatusMutation.mutate({ userId, isActive })
          }
          onDelete={(userId) => deleteUserMutation.mutate(userId)}
        />
      </div>
    </main>
  );
}
