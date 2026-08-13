import type { ApiPayload, SchemaComponents } from './base'

export type Board = SchemaComponents['Board']
export type BoardDetail = SchemaComponents['BoardDetail']
export type PatchedBoard = SchemaComponents['PatchedBoard']
export type PaginatedBoardList = SchemaComponents['PaginatedBoardList']

export type BoardPayload = ApiPayload<Board>