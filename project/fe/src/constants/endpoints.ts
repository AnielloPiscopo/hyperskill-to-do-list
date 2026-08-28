const TASK_BASE_URL = '/tasks/'
const BOARD_BASE_URL = '/boards/'
const AUTH_BASE_URL = '/auth/'

export const TASK_ENDPOINTS = {
    list: TASK_BASE_URL,
    detail: (id: number) => TASK_BASE_URL + id + "/",
    archive: (id: number) => TASK_BASE_URL + id + "/archive/",
    restore: (id: number) => TASK_BASE_URL + id + "/restore/",
    archiveAll: TASK_BASE_URL + "archive-all/",
    restoreAll: TASK_BASE_URL + "restore-all/",
    deleteAll: TASK_BASE_URL + "delete-all/",
    move: TASK_BASE_URL + 'move/'
}

export const BOARD_ENDPOINTS = {
    list: BOARD_BASE_URL,
    detail: (slug: string) => BOARD_BASE_URL + slug + "/",
    archive: (slug: string) => BOARD_BASE_URL + slug + "/archive/",
    restore: (slug: string) => BOARD_BASE_URL + slug + "/restore/",
    archiveAll: BOARD_BASE_URL + "archive-all/",
    restoreAll: BOARD_BASE_URL + "restore-all/",
    deleteAll: BOARD_BASE_URL + "delete-all/",
}

export const AUTH_ENDPOINTS = {
    login: AUTH_BASE_URL + "login/",
    register: AUTH_BASE_URL + "register/",
    logout: AUTH_BASE_URL + "logout/",
    about: AUTH_BASE_URL + "about/",
    changePassword: AUTH_BASE_URL + "change-password/"
}