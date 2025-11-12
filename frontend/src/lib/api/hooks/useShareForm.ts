import { useState, useEffect } from 'react';
import { ShareFormData, ShareFormErrors } from '@/lib/types/share';
import { validateShareForm } from '@/lib/utils/validation';

interface UseShareFormProps {
  pathDisplay: string;
  isOpen: boolean;
  onShare: (data: ShareFormData) => Promise<void>;
}

export function useShareForm({ pathDisplay, isOpen, onShare }: UseShareFormProps) {
  const [formData, setFormData] = useState<ShareFormData>({
    name: '',
    email: '',
    hard_drive_path_selection: pathDisplay,
  });
  const [formErrors, setFormErrors] = useState<ShareFormErrors>({});
  const [showSuccess, setShowSuccess] = useState(false);

  useEffect(() => {
    resetForm();
  }, [pathDisplay, isOpen]);

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      hard_drive_path_selection: pathDisplay,
    });
    setFormErrors({});
    setShowSuccess(false);
  };

  const handleInputChange = (field: keyof ShareFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (field === 'name' || field === 'email') {
      if (formErrors[field]) {
        setFormErrors(prev => ({ ...prev, [field]: undefined }));
      }
    }
  };

  const handleSubmit = async (): Promise<boolean> => {
    const errors = validateShareForm(formData);
    setFormErrors(errors);
    
    if (Object.keys(errors).length > 0) {
      return false;
    }
    
    try {
      await onShare(formData);
      setShowSuccess(true);
      return true;
    } catch (error) {
      console.log(error);
      return false;
    }
  };

  return {
    formData,
    formErrors,
    showSuccess,
    handleInputChange,
    handleSubmit,
    resetForm,
  };
}
