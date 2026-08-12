import type { SchemaComponents, ApiPayload } from './base'

export type Task = SchemaComponents['Task']
export type PatchedTask = SchemaComponents['PatchedTask']
export type TaskMove = SchemaComponents['TaskMove']
export type PaginatedTaskList = SchemaComponents['PaginatedTaskList']

export type TaskStatus = NonNullable<Task['status']>
export type TaskPriority = NonNullable<Task['priority']>

export type TaskPayload = ApiPayload<Task>

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
    TODO: 'To Do',
    IN_PROGRESS: 'In Progress',
    DONE: 'Done'
}

export const TASK_PRIORITY_LABELS: Record<TaskPriority, string> = {
    HIGH: 'High',
    MEDIUM: 'Medium',
    LOW: 'Low',
    ZERO: 'Zero'
}
