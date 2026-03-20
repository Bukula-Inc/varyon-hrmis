import Form_Controller from "../page/form_controller/index.js";
import HTML_Builder from "../page/html/html_builder.js";

export default class Upload_medical_clearance {
  constructor() {
    this.$applicant = $("#new-career-medical-doc");
    this.builder = new HTML_Builder();
    lite.lite_file_picker.init_file_picker(this.init_submit, this)
  }

  async fetch_data(applicant_details) {
    const applicant = await lite?.connect.x_post("get_applicant_data", {applicant_details: applicant_details,});

    if (applicant.status == lite.status_codes.ok) {
      const data = applicant.data;
      this.$applicant.html(`
        <div class="form-header w-full flex justify-between items-center">
          <h1 class="form-title font-bold text-[19px] mb-5 text-gray-500">Applicant Information</h1>
        </div>

        <div class="form-fields grid grid-cols-3 gap-5 p-4 text-secondary">
          <div>
              ${this.builder.build_form_field({
                id: "applicant_name",
                fieldlabel: "Applicant Name",
                fieldname: "applicant_name",
                fieldtype: "read-only",
                required: false,
                wrapper_class: "w-full",
                placeholder: "",
                columns: 1,
                value: data.applicant.applicant,
                readonly: true
              })}
          </div>

          <div>
              ${this.builder.build_form_field({
                id: "applicant_email",
                fieldlabel: "Applicant Email",
                fieldname: "applicant_email",
                fieldtype: "read-only",
                required: false,
                wrapper_class: "w-full",
                placeholder: "",
                columns: 1,
                value: data.applicant.email,
                readonly: true
              })}
          </div>

          <div>
              ${this.builder.build_form_field({
                id: "contact_no",
                fieldlabel: "Contact No.",
                fieldname: "contact_no",
                fieldtype: "read-only",
                required: false,
                wrapper_class: "w-full",
                placeholder: "",
                columns: 1,
                value: data.applicant.contact_no,
                readonly: true
              })}
          </div>
        </div>
      `);

      const medical_and_police_clearance_docs = `
        <div class="grid grid-cols-2 gap-5 mt-5">
          <div>
              ${this.builder.build_form_field({
                  id: "medical_clearance_file",
                  fieldlabel: "Upload Medical Clearance",
                  fieldname: "medical_clearance_file",
                  fieldtype: "file",
                  required: false,
                  wrapper_class: "w-full",
                  placeholder: "Upload medical form",
                  columns: 1,
              })}
          </div>
          <div>
            ${this.builder.build_form_field({
                id: "auth_of_secricy",
                fieldlabel: "Upload Auth Of Secrecy",
                fieldname: "auth_of_secrice",
                fieldtype: "file",
                required: false,
                wrapper_class: "w-full",
                placeholder: "Upload auth of secrecy",
                columns: 1,
            })}
        </div>
          <div>
              ${this.builder.build_form_field({
                  id: "police_clearance_file",
                  fieldlabel: "Upload Police Clearance",
                  fieldname: "police_clearance_file",
                  fieldtype: "file",
                  required: false,
                  wrapper_class: "w-full",
                  placeholder: "Upload police clearance form",
                  columns: 1,
              })}
          </div>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-center mt-5">
          <button type="button" id="submit-clearance" class="bg-default text-white px-6 py-2 rounded-lg font-semibold">
            Submit
          </button>
        </div>
      `;
      this.$applicant.append(medical_and_police_clearance_docs);
      this.init_submit();
    }
  }
  async init_submit(data) {
      console.log(data);
      const updated = await lite.connect.upload({files: data.file})
      console.log(updated);
      
      $("#submit-clearance").on("click", async () => {
          const medical_clearance_form = $("#medical_clearance_file")[0];
          const police_clearance_form = $("#police_clearance_file")[0];
          const oath_of_secrecy = $("#oath_of_secrecy")[0];
          const medical_form = medical_clearance_form.files[0];
          console.log("test here.....",medical_form);
          
          const police_form = police_clearance_form.files[0];
          const oath_of_secrecy_form = oath_of_secrecy.files[0];
          const applicant_attached_documents = new applicant_attached_documents();
          applicant_attached_documents.append("medical_clearance", medical_form);
          applicant_attached_documents.append("police_clearance", police_form);
          applicant_attached_documents.append("auth_of_secrice", oath_of_secrecy_form);
        try {
          const response = await lite?.connect.x_post("applicant_required_documents", applicant_attached_documents);
          console.log();
          
          if (response.status === lite.status_codes.ok) {
            alert("Files uploaded successfully!");
          } else {
            alert("Failed to upload files. Please try again.");
          }
        } catch (error) {
          console.error("Error uploading files:", error);
        }
      });
    }

  init() {
    const applicantDetails = lite.utils.get_url_parameters("applicant");
    this.fetch_data(applicantDetails);
  }
}
