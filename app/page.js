'use client';
import Image from 'next/image';
import { useState } from 'react';

const Dashboard = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const url = URL.createObjectURL(e.target.files[0]);
    setSelectedFile(file);
    setImage(url);
  };

  const handleSubmit = (e) => {
    setResult(null);
    e.preventDefault();

    if (selectedFile) {
      const formData = new FormData();
      formData.append('image', selectedFile);

      fetch('http://localhost:3000/api/classify', {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => setResult(data))
        .catch((error) => console.error('Error:', error));
    }
  };
  return (
    <div className="bg-slate-100">
      <section className="mt-4 w-full">
        <h1 className="text-xl font-extrabold text-[#f65555]">
          Klasifikasi Penyakit Daun Jagung
        </h1>
        <div className="mt-4 flex w-full flex-row gap-5">
          <div className="w-1/2 max-w-[36rem] rounded-md bg-white p-4 shadow-md">
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label
                  htmlFor="image"
                  className="mb-2 block text-sm font-medium text-gray-700"
                >
                  Input Citra Jagung
                </label>
                <input
                  type="file"
                  id="image"
                  accept="image/*"
                  onChange={handleFileChange}
                  className="w-full rounded-md border border-gray-300 px-3 py-2 text-xs focus:outline-none focus:ring focus:ring-[#f65555]"
                />
              </div>
              <div className="relative mx-auto h-[340px] w-[340px] overflow-hidden">
                <Image
                  src={image || 'next.svg'}
                  width={500}
                  height={500}
                  alt="Picture of the author"
                />

                <p>ini {image}</p>
              </div>
              <div className="mt-5 flex flex-row justify-center gap-6">
                <button
                  type="submit"
                  className="rounded-md bg-[#f65555] px-4 py-2 text-sm text-white duration-200 ease-in-out hover:bg-[#f655554a] hover:text-[#f65555]"
                >
                  Klasifikasi
                </button>
              </div>
            </form>
          </div>
          <div className="flex w-1/2 flex-col gap-6">
            <div className="w-full rounded-md bg-white p-4 text-center shadow-md">
              <h1 className="text-amber-800">Model VGG16 Classifier</h1>
              {result === null ? (
                <h2 className="text-[1.4rem] text-amber-800">classify...</h2>
              ) : (
                <h2 className="text-[1.4rem] font-extrabold text-[#f65555]">
                  {result['classify']}
                </h2>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
