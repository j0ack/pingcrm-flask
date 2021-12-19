export type Contact = {
    id: number,
    name: string,
    organization_id: number,
    organization: Record<string, unknown>,
    first_name: string,
    last_name: string,
    email?: string,
    phone?: string,
    address?: string,
    city?: string,
    region?: string,
    country?: string,
    postal_code?: string,
    deleted_at?: string,
}

export type Organization = {
    id: number,
    name: string,
    email?: string,
    phone?: string,
    address?: string,
    city?: string,
    region?: string,
    country?: string,
    postal_code?: string,
}

export type User = {
    id: number,
    first_name: string,
    last_name: string,
    email?: string,
    photo_path?: string,
    owner?: boolean,
    deleted_at?: string,

}

export type Link = {
    url: string | null,
    label: string,
    active?: boolean,
}

export type SearchFilters = {
    search?: string,
    trashed?: string,
    role?: string,
}
