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
export type ApiPayload<T extends BaseApiInterface, ExtraReadOnlyFiedls extends keyof T> =
    Omit<T, keyof ReadOnlyFields | ExtraReadOnlyFiedls>

/**
 * @package
 */
export type SchemaComponents = components['schemas']