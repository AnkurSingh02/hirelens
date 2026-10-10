"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, FileText, X, CheckCircle } from "lucide-react";

interface ResumeUploaderProps {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

export default function ResumeUploader({
  onFileSelect,
  selectedFile,
}: ResumeUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      const files = e.dataTransfer.files;
      if (files && files[0]) {
        if (files[0].type === "application/pdf") {
          onFileSelect(files[0]);
        }
      }
    },
    [onFileSelect]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files[0]) {
        onFileSelect(files[0]);
      }
    },
    [onFileSelect]
  );

  return (
    <AnimatePresence mode="wait">
      {selectedFile ? (
        <motion.div
          key="file-selected"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="border border-green-500/30 rounded-xl p-6 bg-green-500/5"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 300, delay: 0.2 }}
                className="p-2 bg-green-500/20 rounded-lg"
              >
                <CheckCircle className="h-6 w-6 text-green-400" />
              </motion.div>
              <div>
                <motion.p
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  className="text-white font-medium"
                >
                  {selectedFile.name}
                </motion.p>
                <p className="text-slate-400 text-sm">
                  {(selectedFile.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.1, rotate: 90 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => onFileSelect(null)}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
            >
              <X className="h-5 w-5 text-slate-400" />
            </motion.button>
          </div>
        </motion.div>
      ) : (
        <motion.div
          key="upload-zone"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          onDragEnter={handleDragIn}
          onDragLeave={handleDragOut}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`
            relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
            transition-all duration-300 overflow-hidden
            ${
              isDragging
                ? "border-blue-500 bg-blue-500/10 scale-[1.02]"
                : "border-slate-700 hover:border-slate-500 bg-slate-800/30 animate-breathe"
            }
          `}
        >
          {/* Hover glow effect */}
          <motion.div
            className="absolute inset-0 bg-linear-to-br from-blue-500/5 to-purple-500/5 opacity-0"
            whileHover={{ opacity: 1 }}
          />

          <input
            type="file"
            accept=".pdf"
            onChange={handleFileInput}
            className="hidden"
            id="resume-upload"
          />
          <label htmlFor="resume-upload" className="cursor-pointer relative z-10">
            <motion.div
              animate={isDragging ? { scale: 1.2, y: -5 } : { scale: 1, y: 0 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              <Upload
                className={`h-12 w-12 mx-auto mb-4 transition-colors ${
                  isDragging ? "text-blue-400" : "text-slate-500"
                }`}
              />
            </motion.div>
            <p className="text-white font-medium text-lg mb-1">
              {isDragging ? "Drop it here!" : "Drop your resume here"}
            </p>
            <p className="text-slate-400">
              or click to browse (PDF only, max 10MB)
            </p>
          </label>
        </motion.div>
      )}
    </AnimatePresence>
  );
}