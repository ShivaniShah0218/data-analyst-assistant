import {useState} from "react";
import axios from "axios";

const FileUpload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [output, setOutput] = useState<string | null>(null);
    const [loading, setLoading]=useState(false);
    const [error, setError] =  useState<string | null>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files){
            setFile(event.target.files[0]);
        }

    };

    const handleUpload = async() => {
        if (!file){
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        setLoading(true);
        setError(null);

        try{
            const response = await axios.post("http://localhost:8000/upload-csv/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setOutput(response.data.output);
        }catch(err){
            console.error(err);
            setError("Error uploading the file!");
        }finally{
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Upload CSV File for Processing</h2>
            <input type="file" accept=".csv" onChange={handleFileChange}/>
            <button onClick={handleUpload} disabled={loading}>
                {loading ? "Processing... ": "Upload and Process"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
            {output && <pre>{output}</pre>}
        </div>
    );

};

export default FileUpload;
