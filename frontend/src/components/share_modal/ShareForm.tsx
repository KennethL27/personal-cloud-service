import React from 'react';
import { ShareFormData, ShareFormErrors } from '@/lib/types/share';
import { FormInput } from './FormInput';

interface ShareFormProps {
  formData: ShareFormData;
  formErrors: ShareFormErrors;
  loading: boolean;
  onInputChange: (field: keyof ShareFormData, value: string) => void;
  onSubmit: (e: React.FormEvent) => void;
  onCancel: () => void;
}

export function ShareForm({
  formData,
  formErrors,
  loading,
  onInputChange,
  onSubmit,
  onCancel,
}: ShareFormProps) {
  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <FormInput
        id="name"
        label="Name"
        type="text"
        value={formData.name}
        onChange={(value) => onInputChange('name', value)}
        error={formErrors.name}
        placeholder="Enter recipient's name"
        required
      />

      <FormInput
        id="email"
        label="Email"
        type="email"
        value={formData.email}
        onChange={(value) => onInputChange('email', value)}
        error={formErrors.email}
        placeholder="Enter recipient's email"
        required
      />

      <FormInput
        id="path"
        label="Path to Share"
        type="text"
        value={formData.hard_drive_path_selection}
        onChange={() => {}}
        disabled
        helperText="This path will be shared with the recipient"
      />

      <div className="flex gap-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors cursor-pointer"
          disabled={loading}
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={loading}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
        >
          {loading ? 'Sharing...' : 'Share'}
        </button>
      </div>
    </form>
  );
}
