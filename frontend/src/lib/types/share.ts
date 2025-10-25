// frontend/src/lib/types/share.ts

export interface ShareFormData {
    name: string;
    email: string;
    hard_drive_path_selection: string;
  }
  
export interface ShareFormErrors {
    name?: string;
    email?: string;
}
