const TASK_BASE_URL = '/tasks/'
const BOARD_BASE_URL = '/board/'
const AUTH_BASE_URL = '/auth/'

export const TASK_ENDPOINTS = {
    list: TASK_BASE_URL,
    detail: (id: number) => TASK_BASE_URL + id + "/",
    archive: (id: number) => TASK_BASE_URL + id + "/archive/",
    restore: (id: number) => TASK_BASE_URL + id + "/restore/",
    archiveAll: TASK_BASE_URL + "archive-all/",
    restoreAll: TASK_BASE_URL + "restore-all/",
    move: TASK_BASE_URL + 'move/'
}

export const BOARD_ENDPOINTS = {
    list: BOARD_BASE_URL,
    detail: (id: number) => BOARD_BASE_URL + id + "/",
    archive: (id: number) => BOARD_BASE_URL + id + "/archive/",
    restore: (id: number) => BOARD_BASE_URL + id + "/restore/",
    archiveAll: BOARD_BASE_URL + "archive-all/",
    restoreAll: BOARD_BASE_URL + "restore-all/",
}

export const AUTH_ENDPOINTS = {
    login: AUTH_BASE_URL + "login/",
    register: AUTH_BASE_URL + "register/",
    logout: AUTH_BASE_URL + "logout/",
    about: AUTH_BASE_URL + "about/",
    changePassword: AUTH_BASE_URL + "change-password/"
}