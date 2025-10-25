import React from 'react';
import { ShareFormData } from '@/lib/types/share';
import { useShareForm } from '@/lib/api/hooks/useShareForm';
import { ModalHeader } from './ModalHeader';
import { ErrorAlert } from './ErrorAlert';
import { SuccessMessage } from './SuccessMessage';
import { ShareForm } from './ShareForm';

interface ShareModalProps {
  isOpen: boolean;
  onClose: () => void;
  pathDisplay: string;
  onShare: (data: ShareFormData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

export function ShareModal({
  isOpen,
  onClose,
  pathDisplay,
  onShare,
  loading,
  error,
}: ShareModalProps) {
  const {
    formData,
    formErrors,
    showSuccess,
    handleInputChange,
    handleSubmit,
    resetForm,
  } = useShareForm({ pathDisplay, isOpen, onShare });

  if (!isOpen) return null;

  const handleClose = () => {
    resetForm();
    onClose();
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await handleSubmit();
  };

  return (
    <div className="fixed inset-0 bg-black/50 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-500 rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <ModalHeader showSuccess={showSuccess} onClose={handleClose} />
        
        <ErrorAlert error={error} />

        {showSuccess ? (
          <SuccessMessage
            pathDisplay={pathDisplay}
            recipientName={formData.name}
            onClose={handleClose}
          />
        ) : (
          <ShareForm
            formData={formData}
            formErrors={formErrors}
            loading={loading}
            onInputChange={handleInputChange}
            onSubmit={handleFormSubmit}
            onCancel={handleClose}
          />
        )}
      </div>
    </div>
  );
}
