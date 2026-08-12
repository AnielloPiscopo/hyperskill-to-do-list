import type { components } from '@/schema/api-schema'

interface ReadOnlyFields {
    id: number
    created_at: string
    updated_at: string
}

export interface BaseApiInterface extends ReadOnlyFields {
}



export type ApiPayload<T extends BaseApiInterface> = Omit<T, keyof ReadOnlyFields>
export type SchemaComponents = components['schemas']