import type { components } from '@/schema/api-schema'

interface ReadOnlyFields {
    id: number
    created_at: string
    updated_at: string
}

/**
 * @package
 */
export interface BaseApiInterface extends ReadOnlyFields {
}


/**
 * @package
 */
export type ApiPayload<T extends BaseApiInterface> = Omit<T, keyof ReadOnlyFields>

/**
 * @package
 */
export type SchemaComponents = components['schemas']